#!/usr/bin/env python3
import os
import sys
import argparse
from PIL import Image # Linux package python-imaging may include python-pillow

parser = argparse.ArgumentParser(description="Converts a 16-color PNG to a Fairytale/Cocktail Soft GPC.")
parser.add_argument("filename", help="PNG file to convert")
parser.add_argument("-x", type=int, default=0, help="In-game X coordinate, default 0")
parser.add_argument("-y", type=int, default=0, help="In-game Y coordinate, default 0")
args = parser.parse_args()

# The encoding process is:
# - Ensure bitmap is padded to a 4-byte (8px) boundary
# - Split bitmap so that the full bitplanes are side by side in a new bitmap
# - Allow an extra byte at start of each row for the horizontal interlacing value
# - Determine best vertical interlacing, shuffle bitmap rows
# - Apply vertical XOR from bottom to top, except the topmost row
# - For each row: Determine best horizontal interlacing/XOR, apply it
# - Run flag A/flag B compression to pack all 00 bytes
#
# The most useful interlacing values both ways are: 1, 2, 4; and 0 for horizontal only.
# However, original GPC files do use a wide variety of odd interlacing values...
# Optimal encoding: try all interlacing pairs for the whole image, select the one that
# produces the smallest output. Maximise well-aligned 00 x 8 runs, and secondarily
# maximise 00 bytes elsewhere, including the horizontal filter bytes.
#
# Also maximise final run of 00's, since they can be omitted from encoding. Although many
# original GPC files don't omit these, so it may or may not work...

global hrz_steps
#hrz_steps = [0, 1, 2, 4, 8, 0x10, 0x20, 0x26, 0x2A, 0x36, 0x38, 0x40, 0x49, 0x4D, 0x50]
hrz_steps = range(0x51)

def MakeInterlaceTable(size, steps):
	table = {}
	for step in steps:
		if step == 0: continue
		result = [None] * size
		start = 0
		writeofs = 0
		while start < step:
			i = start
			while i < size:
				result[writeofs] = i
				writeofs += 1
				i += step
			start += 1
		table[step] = result
	return table

def VerticalIX(srcview, workview, w, h, vrt_list):
	stride = w >> 1
	# Interlace row data from the split planes into workview (workbuf).
	writeofs = 1
	for row in vrt_list:
		readofs = row * stride
		workview[writeofs:writeofs + stride] = srcview[readofs:readofs + stride]
		writeofs += stride + 1

	if h == 1: return
	# Xor every row but the topmost in workview (workbuf) with the row above it. (backward scan)
	writeofs -= 1
	for i in range((stride + 1) * (h - 1)):
		writeofs -= 1
		workview[writeofs] ^= workview[writeofs - stride - 1]

def HorizontalIX(workview, rowbuf, w, h, hrz_lookup):
	stride = w >> 1
	rowstart = 1
	# Whether scanning forward or backward, it's a bit hard to handle flag A and flag B bytes,
	# since they're out of sync with the scan pointer...
	# Try to at least count 0 bytes sensibly.
	for y in range(h):
		# Generate copies of this row with each horizontal interlaced XOR value.
		rowbuf[0][1:1 + stride] = workview[rowstart:rowstart + stride]
		for hrz in hrz_steps:
			if hrz == 0: continue
			lastbyte = 0
			lookup = hrz_lookup[hrz]
			for x in range(stride):
				nextbyte = workview[rowstart + lookup[x]]
				rowbuf[hrz][lookup[x] + 1] = lastbyte ^ nextbyte
				lastbyte = nextbyte

		# Estimate how many bits each row would compress into.
		bestbits = 0xFFFF
		#print("===========")
		for hrz in hrz_steps:
			row = rowbuf[hrz]
			#print(row.hex())
			nullrun = 0
			bits = 0
			align = rowstart
			for x in range(stride + 1):
				if row[x] != 0:
					bits += 8
					nullrun = 0
				else:
					nullrun = (nullrun + 1) & 7
					if nullrun == 0:
						bits -= 8
				align = (align + 1) & 7
				if align == 0:
					nullrun = 0
			if bits < bestbits:
				bestbits = bits
				besthrz = hrz

		# Overwrite the current row in workview (workbuf) with the hopefully best XOR'ed row.
		#print("row",y,"using hrz",besthrz)
		workview[rowstart - 1:rowstart + stride] = rowbuf[besthrz]
		rowstart += stride + 1

def Encode(workview, finalview):
	# Work from end to beginning, since this allows building and writing the flag values in
	# a single linear pass. Otherwise would have to keep poking flag values into the past...
	flagA = 0
	flagB = 0
	readofs = len(workview)
	writeofs = len(finalview)
	# Since working from the end, the last section may not be a neat multiple of 8 or 64.
	# This can be handled by initialising flag A and flag B as if there were extra 00 bytes
	# until the next 64-byte boundary.
	# Each flag A bit describes 8 bytes; the whole thing describes 64 bytes.
	# If there are 63 bytes to go, we've only started building flag A, so it has all 8 bits left.
	# If there are 50 bytes to go, that's enough to knock flag A down to 7 remaining bits...
	# If there's 1 byte to go, flag A just has 1 remaining bit also...
	flagAbitsleft = ((readofs + 7) >> 3) & 7
	if flagAbitsleft == 0: flagAbitsleft = 8
	# Each flag B bit describes 1 byte.
	flagBbitsleft = readofs & 7
	if flagBbitsleft == 0: flagBbitsleft = 8

	while readofs != 0:
		flagB >>= 1
		readofs -= 1
		if workview[readofs] != 0:
			# Non-zero byte: output as literal, add a 1 bit in flag B.
			writeofs -= 1
			finalview[writeofs] = workview[readofs]
			flagB |= 0x80
		flagBbitsleft -= 1
		if flagBbitsleft == 0:
			flagBbitsleft = 8
			flagA >>= 1
			if flagB != 0:
				# Some literals were present. Output flag B, add a 1 bit in flag A.
				writeofs -= 1
				finalview[writeofs] = flagB
				flagA |= 0x80
			flagAbitsleft -= 1
			if flagAbitsleft == 0:
				flagAbitsleft = 8
				writeofs -= 1
				finalview[writeofs] = flagA

	return writeofs

def Compress(srcbuf, w, h):
	stride = w >> 1
	hrz_lookup = MakeInterlaceTable(stride, hrz_steps)
	vrt_lookup = MakeInterlaceTable(h, [1, 2, 4])
	rowbuf = {}
	for hrz in hrz_steps:
		rowbuf[hrz] = bytearray(stride + 1)
		rowbuf[hrz][0] = hrz
	workbuf = bytearray((stride + 1) * h)
	workview = memoryview(workbuf) # direct access to bytes to avoid copy on slice
	srcview = memoryview(srcbuf)
	finalbuf = bytearray(len(workview) * 8 // 7) # preallocate for worst-case output size
	finalview = memoryview(finalbuf)
	bestofs = 0
	# Generate a compressed buffer for each vertical interlacing value, keep the smallest one.
	for vrt in [2, 1, 4]:
		print("... trying vrt",vrt,"...")
		VerticalIX(srcview, workview, w, h, vrt_lookup[vrt])
		HorizontalIX(workview, rowbuf, w, h, hrz_lookup)
		writeofs = Encode(workview, finalview)
		if writeofs > bestofs:
			bestbuf = finalbuf[writeofs:]
			bestofs = writeofs
			bestvrt = vrt
	return bestbuf, bestvrt

if args.filename.lower().endswith('.gpc'):
	print("Error: This tool converts PNG to GPC, not GPC to PNG.")
	print("Please provide a PNG file as input.")
	exit(1)

with Image.open(args.filename) as img:
	print("Read as", img.format, img.size, img.mode)
	if img.mode != 'P':
		print("Image must have a palette")
		exit(2)
	palette = img.getpalette()
	if len(palette) < 48:
		palette.extend(bytearray(48 - len(palette)))
	elif len(palette) > 48:
		palette = palette[0:48]

	if (img.width > 640):
		print("Image width should be no larger than 640 pixels")
		exit(4)
	if (img.height > 400):
		print("Image height should be no larger than 400 pixels")
		exit(4)
	basename, ext = os.path.splitext(img.filename)

	# Header
	outbuf = bytearray("PC98)GPCFILE   ".encode()) # sig
	outbuf += bytearray(5) # terminating null and vertical interlacing dword, tbd later
	outbuf += bytearray([0x30, 0, 0, 0, 0x54, 0, 0, 0]) # palette and image pointers
	outbuf += bytearray(20) # padding to start of palette

	outbuf += bytearray([16, 0, 2, 0]) # palette dimensions
	for i in range(0, 48, 3):
		outbuf += bytearray([(palette[i] & 0xF0) | (palette[i + 2] >> 4), palette[i + 1] >> 4])

	# Image dimensions.
	w = img.width
	h = img.height
	outbuf += bytearray([w & 0xFF, w >> 8, h & 0xFF, h >> 8, 0, 0, 0, 0, 4, 0, args.x & 0xFF, args.x >> 8, args.y & 0xFF, args.y >> 8, 0, 0])

	if (img.width % 8) != 0:
		# Pad width to a multiple of 8 with transparent 0's.
		newimg = Image.new(img.mode, ((img.width + 7) & 0xFFF8, img.height), 16)
		newimg.paste(img, (0, 0))
		img = newimg
		w = img.width

	# The bitmap is an array of individual 4/8 bpp pixel values in scanline order.
	bitmap = img.getdata()

	# Separate the bitplanes into four plane buffers, 8 1-bit pixels in each byte, and place
	# the buffers side by side into a single bitmap.
	planebuf = bytearray(len(bitmap) >> 1)
	planewidth = w >> 3
	ofs = 0
	octet = [0] * 4
	x = 0
	for j in range(0, len(bitmap), 8):
		for l in range(j, j + 8):
			for i in range(4):
				octet[i] = (octet[i] << 1) | ((bitmap[l] >> i) & 1)
		o = ofs
		for i in range(4):
			planebuf[o] = octet[i]
			o += planewidth
			octet[i] = 0
		ofs += 1
		x += 8
		# Next row.
		if x >= w:
			x = 0
			ofs += planewidth * 3

	compressed_data, bestvrt = Compress(planebuf, w, h)
	print("Using vertical interlacing " + str(bestvrt) + ", compressed to", len(compressed_data), "bytes + header.")

	# Stash the vertical interlacing value in the header.
	outbuf[0x10] = bestvrt & 0xFF
	outbuf[0x11] = bestvrt >> 8
	# Stash compressed size in the header.
	outbuf[0x58] = len(compressed_data) & 0xFF
	outbuf[0x59] = len(compressed_data) >> 8
	# Stash the compressed bytes.
	outbuf += compressed_data

	outputname = basename + '.gpc'
	print("writing into", outputname)
	with open(outputname, 'wb') as f:
		f.write(outbuf)

exit(0)
