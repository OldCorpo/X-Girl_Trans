(mes
 (meta (engine 'ADV) (charset "pc98") (extraop #t))
 (seg*
  ((cmd 206) 0 0)
  ((cmd 206) 1 1)
  (mouse 3 0 0)
  ((cmd 203) 1 1)
  ((cmd 203) 5 16)
  (text-frame 0 0 79 399)
  (load-mem "tcm¥rzonettl.tcm" 256)
  (exec-mem 256)
  (text-color 15 14 14)
  ((cmd 204))
  (load-mem "tcm¥acte.tcm" 256)
  (exec-mem 256 "I")
  (load-mem "tcm¥reclickh.tcm" 3072)
  (load-mem "tcm¥mousecsr.tcm" 3968)
  (load-mem "gpc¥window.chp" 4480)
  (load-mem "tcm¥mltwh.tcm" 4768)
  (load-mem "tcm¥palch.tcm" 7072)
  (load-mem "tcm¥gpcpalch.tcm" 7936)
  (load-mem "tcm¥mbuff.tcm" 9504)
  (load-mem "tcm¥pushpalh.tcm" 11680)
  (load-mem "tcm¥quakeh.tcm" 12288)
  (load-mem "tcm¥tmaskh.tcm" 14080)
  (load-mem "tcm¥mcsranmh.tcm" 18688)
  (load-mem "tcm¥mnjcount.tcm" 24576)
  (exec-mem 24576 0 0 2 5 0 1 "clm¥mnj7seg.dat")
  (load-mem "tcm¥mnjcsr.tcm" 25984)
  (load-mem "tcm¥db2cls.tcm" 27008)
  (load-mem "tcm¥whiteh.tcm" 27648)
  (load-mem "tcm¥cappear.tcm" 28672)
  (load-mem "tcm¥deltar.tcm" 29184)
  (exec-mem 18688 0 "icon¥iconmo.chr")
  (exec-mem 18688 1 2 "A0 T3 A1 T3")
  (exec-mem 18688 1 3 "A2 T3 A3 T3")
  (exec-mem 18688 1 4 "A4 T3 A5 T3")
  (exec-mem 18688 1 5 "A6 T3 A7 T3")
  (exec-mem 18688 1 6 "A8 T3 A9 T3")
  (exec-mem 18688 1 7 "A10 T3 A11 T3")
  (exec-mem 18688 1 8 "A12 T3 A13 T3")
  (exec-mem 18688 1 9 "A14 T3 A15 T3")
  (exec-mem 18688 1 10 "A16 T3 A17 T3")
  (exec-mem 18688 1 11 "A18 T3 A19 T3")
  (exec-mem 18688 1 12 "A20 T3 A21 T3")
  (sound 'se "uso¥xg.se")
  (define-proc 0 (<> (exec-mem 3968 103) (exec-mem 3072 0)))
  (define-proc 1 (<> (exec-mem 3968 104) (exec-mem 3072 2) (exec-mem 3072 1)))
  (define-proc 3 (<> (exec-mem 14080 1 80 34 80 34 24 4 135 71 8 30)))
  (define-proc 4
    (<>
     (proc 0)
     (branch-reg
      991
      (</> (/ (exec-mem 256 "P 6 9 16")) (/ (exec-mem 256 "P 7 52 16"))))
     (proc 1)))
  (define-proc 5
    (<>
     (branch-reg
      991
      (</> (/ (exec-mem 256 "P 8 6 0")) (/ (exec-mem 256 "P 9 71 0"))))))
  (define-proc 6
    (<>
     (exec-mem 256 "G 8 6 0 3 279")
     (exec-mem 256 "G 9 71 0 3 279")
     (proc 2)))
  (define-proc 7 (<> (exec-mem 3968 103) (exec-mem 25984 2 0) (sound 'se 2)))
  (define-proc 8
    (<> (exec-mem 3968 104) (exec-mem 25984 2 1) (exec-mem 3072 2)))
  (define-proc 9
    (<>
     (exec-mem 12288 3 0 1 5 0)
     (exec-mem 11680 0)
     (exec-mem 27648 2 2)
     (exec-mem 3072 2)))
  (define-proc 10
    (<>
     (exec-mem 3968 103)
     (exec-mem 3072 0)
     (exec-mem 256 "G 10 8 304 64 80")
     (exec-mem 9504 "C gpc¥messwaku.gpc,GPC")
     (image-mem 1 0)))
  (define-proc 11
    (<>
     (exec-mem 256 "P 10 8 304")
     (exec-mem 3968 104)
     (exec-mem 3072 2)
     (exec-mem 3072 1)))
  (define-proc 12
    (<> (exec-mem 256 "G 6 9 16 19 264") (exec-mem 256 "G 7 52 16 19 264")))
  (define-proc 2
    (<>
     (branch-reg
      991
      (</>
       (/ (exec-mem 256 "P 5 6 0") (exec-mem 256 "P 7 52 16"))
       (/ (exec-mem 256 "P 5 71 0") (exec-mem 256 "P 6 9 16"))))))
  ((cmd 209) 0 0)
  (image-file "gpc¥waku.gpc")
  (image-mem 0 3)
  (text-frame 0 0 79 399)
  (text-reset 14)
  ((cmd 209) 1 0)
  ((cmd 203) 5 0)
  (exec-mem 256 "G 1 0 0 18 194")
  (exec-mem 4768 0 0 18 8 1 0 0 4480 4480 1 0)
  (menu1
   1
   8
   1
   24
   1
   40
   (</> (/ (text "　ＦＭ音源内蔵　")) (/ (str " 　音源ボード　 ")) (/ (text "　　音源無し　　"))))
  (exec-mem 256 "P 1 0 0")
  (if (</>
       (// (? (= S 0)) (nop@) (set-var O 0))
       (// (? (= S 1)) (nop@) (set-var O 1))
       (// (? (= S 2)) (nop@) (set-var O 2))))
  (mes-jump "mes¥x_menu.mes")))