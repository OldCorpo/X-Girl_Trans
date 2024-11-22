(mes
 (meta (engine 'ADV) (charset "pc98") (extraop #t))
 (seg*
  ((cmd 209) 0 5)
  (image-file "gpc¥waku.gpc")
  (image-mem 0 3)
  (nop@)
  (set-reg 1002 #f)
  (define-proc 19 (<> ((cmd 209) 0 5)))
  (define-proc 18 (<> ((cmd 209) 1 5)))
  (exec-mem 256 "I")
  (exec-mem 256 "S 0")
  (load-mem "clm¥xgmode.clm" 32768)
  (text-frame 0 0 79 399)
  (text-reset 14)
  ((cmd 209) 1 0)
  (exec-mem 3072 0)
  (exec-mem 3968 101 0 0 639 399)
  ((cmd 203) 5 16)
  (exec-mem 256 "G 1 4 64 20 200")
  (exec-mem 4768 4 8 20 20 1 0 0 4480 4480 1 0)
  (menu1
   5
   72
   5
   88
   5
   104
   5
   120
   5
   136
   5
   152
   5
   168
   5
   184
   5
   200
   (</>
    (/ (text "　　エイプリル　　"))
    (/ (str "　　 レイファ 　　"))
    (/ (str "　　　 ナナ 　　　"))
    (/ (text "　　　ミツコ　　　"))
    (/ (text "　　　エリコ　　　"))
    (/ (text "　　　プリス　　　"))
    (/ (text "　　　アンナ　　　"))
    (/ (text "全てのキャラを見る"))
    (/ (text "　　キャンセル　　"))))
  (exec-mem 256 "P 1 4 64")
  (exec-mem 3968 101 639 399 639 399)
  (exec-mem 3072 0)
  (if (</>
       (// (? (= S 0)) (nop@) (set-reg 1002 #f) (mes-jump "mes¥xcg_epi.mes"))
       (// (? (= S 1)) (nop@) (set-reg 1002 #f) (mes-jump "mes¥xcg_reif.mes"))
       (// (? (= S 2)) (nop@) (set-reg 1002 #f) (mes-jump "mes¥xcg_nana.mes"))
       (// (? (= S 3)) (nop@) (set-reg 1002 #f) (mes-jump "mes¥xcg_mitu.mes"))
       (// (? (= S 4)) (nop@) (set-reg 1002 #f) (mes-jump "mes¥xcg_eric.mes"))
       (// (? (= S 5)) (nop@) (set-reg 1002 #f) (mes-jump "mes¥xcg_pric.mes"))
       (// (? (= S 6)) (nop@) (set-reg 1002 #f) (mes-jump "mes¥xcg_anna.mes"))
       (// (? (= S 7)) (nop@) (set-reg 1002 #t) (mes-jump "mes¥xcg_epi.mes"))
       (//
        (? (= S 8))
        (exec-mem 3968 101 0 0 639 399)
        ((cmd 209) 0 5)
        ((cmd 203) 5 0)
        (mes-jump "mes¥x_menu.mes"))
       (//
        (? (= S 255))
        (exec-mem 3968 101 0 0 639 399)
        ((cmd 209) 0 5)
        ((cmd 203) 5 0)
        (mes-jump "mes¥x_menu.mes"))))))