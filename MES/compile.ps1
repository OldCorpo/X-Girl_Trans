if($args.Length -gt 0){
    forEach($possFile in $args){
        if(-not (Test-Path $possFile)){
            # If file doesn't exist, tell the user clearly and exit
            Write-Warning "FATAL: One of the files you specified ($possFile) doesn't exist.`nPlease make it exist or remove it from the arguments, then try this script again."
            exit -1
        }
    }
    forEach($fileName in $args){
        $fileToCompile = Get-Item $fileName
        ..\juice.exe -c -f $fileToCompile.Name
        $compiledFile = Get-Item "$fileName.mes"
        Rename-Item $compiledFile ($compiledFile.Name.Substring(0,$compiledFile.Name.Length-8))
    }
    exit
}

forEach($msgFile in Get-ChildItem "*.rkt"){
..\juice.exe -c $msgFile.Name
}
forEach($msgFile in Get-ChildItem "*.rkt.mes"){
Rename-Item $msgFile ($msgFile.Name.Substring(0,$msgFile.Name.Length-8))
}