# Tabelas do quick-check VIA

## Prevalencia por codigo

| codigo | familia | severidade | achados | artefatos_com_achado | n | share_artefatos | media_por_artefato | media_por_servico |
|---|---|---|---|---|---|---|---|---|
| D03 | completude | baixa | 41 | 41 | 356 | 0.115169 | 0.115169 | 0.018304 |
| D04 | coerencia | alta | 297 | 271 | 356 | 0.761236 | 0.834270 | 0.132589 |
| D05 | coerencia | alta | 89 | 36 | 356 | 0.101124 | 0.250000 | 0.039732 |
| D06 | coerencia | media | 12 | 12 | 356 | 0.033708 | 0.033708 | 0.005357 |
| D07 | coerencia | media | 0 | 0 | 356 | 0.000000 | 0.000000 | 0.000000 |
| D11 | interface | media | 1977 | 353 | 356 | 0.991573 | 5.553371 | 0.882589 |
| D12 | interface | baixa | 93 | 93 | 356 | 0.261236 | 0.261236 | 0.041518 |

## Por modelo

| llm | n | structural_defect_rate | defect_rate | cycle_density | gini | endpoints_per_responsibility | d11_share | stability_edges | f1_inter |
|---|---|---|---|---|---|---|---|---|---|
| Claude | 116 | 0.139922 | 1.179474 | 0.121449 | 0.160575 | 0.150494 | 0.989943 | 0.831770 | 0.831133 |
| DeepSeek | 120 | 0.265665 | 1.220050 | 0.183869 | 0.180968 | 0.184203 | 0.902083 | 0.779148 | 0.829087 |
| Gemini | 120 | 0.232242 | 1.163611 | 0.134276 | 0.118202 | 0.271970 | 0.873442 | 0.714183 | 0.877238 |

## Por configuracao

| config | n | structural_defect_rate | defect_rate | cycle_density | gini | endpoints_per_responsibility | d11_share | stability_edges | f1_inter |
|---|---|---|---|---|---|---|---|---|---|
| C0 | 72 | 0.246991 | 1.204497 | 0.158895 | 0.148281 | 0.220079 | 0.900794 | 0.819054 | 0.831879 |
| C1 | 72 | 0.175579 | 1.154845 | 0.137517 | 0.153019 | 0.202186 | 0.927827 | 0.805450 | 0.876706 |
| C2 | 72 | 0.219643 | 1.206647 | 0.149306 | 0.153815 | 0.195921 | 0.933862 | 0.768348 | 0.868171 |
| C3 | 72 | 0.221462 | 1.183895 | 0.137202 | 0.160484 | 0.206213 | 0.908366 | 0.767714 | 0.806010 |
| C4 | 68 | 0.202871 | 1.189216 | 0.151401 | 0.150059 | 0.188843 | 0.935224 | 0.707711 | 0.847226 |

## Por sistema

| system | n | structural_defect_rate | defect_rate | cycle_density | gini | endpoints_per_responsibility | d11_share | stability_edges | f1_inter |
|---|---|---|---|---|---|---|---|---|---|
| 7ep | 45 | 0.259127 | 1.209127 | 0.085714 | 0.176288 | 0.184053 | 0.950000 | 0.878108 | 0.957707 |
| AcmeAir | 45 | 0.088889 | 1.048148 | 0.059259 | 0.144229 | 0.204257 | 0.959259 | 0.860918 | 0.950416 |
| Cargo-Tracker | 45 | 0.270053 | 1.317936 | 0.172831 | 0.127932 | 0.223944 | 0.871243 | 0.509040 | 0.620529 |
| DayTrader7 | 45 | 0.298519 | 1.291640 | 0.181058 | 0.177966 | 0.159691 | 0.993122 | 0.680638 | 0.805120 |
| JPetStore | 44 | 0.208333 | 1.204546 | 0.196970 | 0.211779 | 0.174213 | 0.996212 | 0.897283 | 0.883255 |
| Jokul | 44 | 0.193182 | 1.162879 | 0.155303 | 0.094373 | 0.159369 | 0.969697 | 0.807792 | 0.911525 |
| PetClinic | 44 | 0.276136 | 1.519318 | 0.247727 | 0.060444 | 0.183954 | 1.000000 | 0.817424 | 0.878614 |
| TNTConcept | 44 | 0.111742 | 0.746212 | 0.077651 | 0.232004 | 0.333839 | 0.626894 | 0.747805 | 0.761852 |

## Correlacoes por sistema

| scope | system | metric | n | rho | ci_low | ci_high |
|---|---|---|---|---|---|---|
| system | 7ep | structural_defect_rate | 45 | -0.421022 | -0.671446 | -0.126582 |
| system | 7ep | defect_rate | 45 | -0.131065 | -0.456002 | 0.191284 |
| system | 7ep | cycle_density | 45 | -0.071916 | -0.409795 | 0.276583 |
| system | 7ep | gini | 45 | -0.301590 | -0.598739 | 0.039213 |
| system | 7ep | endpoints_per_responsibility | 45 | -0.191433 | -0.484935 | 0.112095 |
| system | 7ep | stability_edges | 45 | 0.549515 | 0.285256 | 0.757154 |
| system | 7ep | d11_share | 45 | 0.407504 | 0.110020 | 0.667394 |
| system | AcmeAir | structural_defect_rate | 45 | -0.874130 | -0.980690 | -0.742702 |
| system | AcmeAir | defect_rate | 45 | -0.677054 | -0.864849 | -0.459418 |
| system | AcmeAir | cycle_density | 45 | -0.681328 | -0.899880 | -0.418045 |
| system | AcmeAir | gini | 45 | -0.779047 | -0.864740 | -0.644014 |
| system | AcmeAir | endpoints_per_responsibility | 45 | 0.345612 | -0.034681 | 0.691226 |
| system | AcmeAir | stability_edges | 45 | 0.495759 | 0.189522 | 0.728349 |
| system | AcmeAir | d11_share | 45 | 0.215459 | -0.184007 | 0.554377 |
| system | Cargo-Tracker | structural_defect_rate | 45 | -0.080324 | -0.398886 | 0.261042 |
| system | Cargo-Tracker | defect_rate | 45 | -0.007877 | -0.341883 | 0.358567 |
| system | Cargo-Tracker | cycle_density | 45 | 0.441014 | 0.176153 | 0.667378 |
| system | Cargo-Tracker | gini | 45 | -0.323130 | -0.569714 | -0.030441 |
| system | Cargo-Tracker | endpoints_per_responsibility | 45 | 0.139563 | -0.219383 | 0.516594 |
| system | Cargo-Tracker | stability_edges | 45 | 0.174208 | -0.174205 | 0.501250 |
| system | Cargo-Tracker | d11_share | 45 | 0.001754 | -0.402472 | 0.374042 |
| system | DayTrader7 | structural_defect_rate | 45 | 0.074603 | -0.291993 | 0.478109 |
| system | DayTrader7 | defect_rate | 45 | 0.104006 | -0.274495 | 0.500178 |
| system | DayTrader7 | cycle_density | 45 | 0.321513 | -0.039504 | 0.636202 |
| system | DayTrader7 | gini | 45 | -0.641385 | -0.809269 | -0.364572 |
| system | DayTrader7 | endpoints_per_responsibility | 45 | 0.621869 | 0.313567 | 0.849424 |
| system | DayTrader7 | stability_edges | 45 | -0.001798 | -0.326547 | 0.337473 |
| system | DayTrader7 | d11_share | 45 | 0.071941 | -0.193149 | 0.340924 |
| system | JPetStore | structural_defect_rate | 44 | 0.402415 | 0.040576 | 0.689479 |
| system | JPetStore | defect_rate | 44 | 0.402415 | 0.040576 | 0.689479 |
| system | JPetStore | cycle_density | 44 | 0.527891 | 0.294165 | 0.707185 |
| system | JPetStore | gini | 44 | -0.019255 | -0.343554 | 0.296040 |
| system | JPetStore | endpoints_per_responsibility | 44 | -0.082210 | -0.456317 | 0.318476 |
| system | JPetStore | stability_edges | 44 | 0.103756 | -0.294313 | 0.486765 |
| system | JPetStore | d11_share | 44 | 0.308417 | 0.245008 | 0.581541 |
| system | Jokul | structural_defect_rate | 44 | -0.085898 | -0.410067 | 0.238692 |
| system | Jokul | defect_rate | 44 | -0.015924 | -0.335646 | 0.299662 |
| system | Jokul | cycle_density | 44 | 0.002066 | -0.321909 | 0.322712 |
| system | Jokul | gini | 44 | -0.162549 | -0.483951 | 0.178163 |
| system | Jokul | endpoints_per_responsibility | 44 | 0.302054 | 0.002053 | 0.556210 |
| system | Jokul | stability_edges | 44 | 0.424453 | 0.118058 | 0.699161 |
| system | Jokul | d11_share | 44 | 0.280820 | 0.091245 | 0.531085 |
| system | PetClinic | structural_defect_rate | 44 | 0.082186 | -0.426678 | 0.528774 |
| system | PetClinic | defect_rate | 44 | 0.082186 | -0.426678 | 0.528774 |
| system | PetClinic | cycle_density | 44 | 0.426014 | 0.000000 | 0.732335 |
| system | PetClinic | gini | 44 | -0.525429 | -0.781299 | -0.234489 |
| system | PetClinic | endpoints_per_responsibility | 44 | 0.447879 | 0.144620 | 0.696734 |
| system | PetClinic | stability_edges | 44 | 0.291882 | 0.011887 | 0.545271 |
| system | PetClinic | d11_share | 44 |  |  |  |
| system | TNTConcept | structural_defect_rate | 44 | -0.554840 | -0.713860 | -0.263572 |
| system | TNTConcept | defect_rate | 44 | 0.324503 | 0.033144 | 0.581486 |
| system | TNTConcept | cycle_density | 44 | 0.440556 | 0.260799 | 0.638227 |
| system | TNTConcept | gini | 44 | -0.132402 | -0.435442 | 0.218001 |
| system | TNTConcept | endpoints_per_responsibility | 44 | -0.435042 | -0.662126 | -0.157755 |
| system | TNTConcept | stability_edges | 44 | -0.029357 | -0.348796 | 0.314354 |
| system | TNTConcept | d11_share | 44 | 0.515858 | 0.234525 | 0.737733 |

## Correlacoes agrupadas

| metric | rho | ci_low | ci_high | n | scope |
|---|---|---|---|---|---|
| structural_defect_rate | -0.106916 | -0.447634 | 0.212419 | 356 | pooled_cluster |
| defect_rate | -0.011112 | -0.443646 | 0.422131 | 356 | pooled_cluster |
| cycle_density | -0.034230 | -0.362055 | 0.375667 | 356 | pooled_cluster |
| gini | -0.310861 | -0.545400 | -0.045426 | 356 | pooled_cluster |
| endpoints_per_responsibility | 0.048383 | -0.285000 | 0.333243 | 356 | pooled_cluster |
| stability_edges | 0.453682 | 0.294834 | 0.548962 | 356 | pooled_cluster |
| d11_share | 0.326544 | 0.045617 | 0.586381 | 356 | pooled_cluster |

## Contrastes focais

| hipotese | comparacao | efeito | ci_low | ci_high | p_raw | p_holm | n_unidades | detalhe |
|---|---|---|---|---|---|---|---|---|
| H1 | rho(F1_inter, defeitos estruturais por serviço) por sistema, mediana | -0.080324 | -0.554840 | 0.082186 | 0.252350 | 0.373926 | 8 | 5 de 8 sistemas com rho negativo; D03-D06, sem D11/D12 |
| H2 | densidade de ciclos C1 - C0 | -0.021379 | -0.052778 | 0.003356 | 0.186963 | 0.373926 | 24 | unidade: sistema x modelo, media das 3 execucoes |
| H3 | endpoints por responsabilidade Gemini - DeepSeek | 0.087768 | 0.062221 | 0.114710 | 0.000200 | 0.000600 | 40 | unidade: sistema x configuracao, media das 3 execucoes |

## Contrastes exploratorios

| codigo | comparacao | efeito | ci_low | ci_high | p_raw | n_unidades | detalhe |
|---|---|---|---|---|---|---|---|
| E1 | C1 - C0, defeitos estruturais | -0.071412 | -0.126472 | -0.024752 | 0.005999 | 24 | exploratorio; p bruto; unidade: sistema x modelo |
| E2 | C1 - C0, F1_inter | 0.044826 | 0.002272 | 0.098951 | 0.074585 | 24 | exploratorio; p bruto; unidade: sistema x modelo |
| E3 | Claude - DeepSeek, defeitos estruturais | -0.126448 | -0.182232 | -0.075694 | 0.000200 | 40 | exploratorio; p bruto; unidade: sistema x configuracao |
| E4 | Claude - DeepSeek, F1_inter | 0.002455 | -0.063277 | 0.064514 | 0.941812 | 40 | exploratorio; p bruto; unidade: sistema x configuracao |
| E5 | Claude - Gemini, defeitos estruturais | -0.093026 | -0.143502 | -0.045675 | 0.000200 | 40 | exploratorio; p bruto; unidade: sistema x configuracao |
| E6 | Claude - Gemini, F1_inter | -0.045695 | -0.085259 | -0.008735 | 0.025595 | 40 | exploratorio; p bruto; unidade: sistema x configuracao |
| E7 | Gemini - DeepSeek, defeitos estruturais | -0.033423 | -0.106905 | 0.036240 | 0.378924 | 40 | exploratorio; p bruto; unidade: sistema x configuracao |
| E8 | Gemini - DeepSeek, F1_inter | 0.048151 | -0.007002 | 0.100768 | 0.089382 | 40 | exploratorio; p bruto; unidade: sistema x configuracao |
