# Copyright (C) 2011 Lukas Lalinsky
# Distributed under the MIT license, see the LICENSE file for details.

import os
import json
import pprint
import difflib
from contextlib import closing
from nose.tools import make_decorator
from acoustid.script import Script
from acoustid.tables import metadata
from acoustid.db import DatabaseContext

TEST_2_LENGTH = 320
TEST_2_FP = 'AQABVtuUZFGShAqO-h9OHD96SvhwBVNCKQnOIYmiIc-ENwF7TDe8Hr0W_AjhvRCP2sfT4DTS7zjyOYeqaI-RSxee5RmaWzhOHnlcaB6HnPgpdE-DkWIH2ysYG_Eh9zJCyfCXGOdw-EGoD2p69IavWOhzMD-a9tBx9FgPVz2qNDvQH3744ISIXRKeHto5_MhyeMtxc-COnYJ_lHLwRAgPvShz_Hga4zd8HD9UKXWOPP3xRLmGnlbQHKfxGPeRvAt6UngMvcF-gkpRi0bUZjGaH6FUHb_xGDt6aHmM__ghfkmH70B4fWiuCj8y8uj3oImZY8d3NFWWHuGF-3hCPEd_uEOyE_nw4w8ueXi24znCHOHxSWtw9BnSBzrSHF2Y4S0e_EioZoh9XMGfo2dqNMeP80aQPM5xGT9efMeTYL-KIqmHdDraHs-P8IcYjoj0I7_Q43iJ9BF64nSKKth2SjG-cvCHH-2OL8txHsUt9HhF4LiK5j16lAf1FkjvQiN55FSOkkOPkmj4GK-OH80eIeyh98HhE_qhPwjzKAV-HJ2OZkd4Q_vhp0d_6Id-_IeWW9CKoP3RKM-Bo3mOfvhxND_6HMgZ6EfXHB-8Q8-iok1znOi-ozmx54P2Dg5V_PCgLxy8KiH6C0cbHU3Ebtiho9Rxw8er47tw7jgRNxl84ziPJ-B1_DiNNClzaGSCvMGPGxePMD5qZYEuAwdTXYSYcIkmodc2nMqg_WgqBk_yBdVx0vCjQD8uhNRxXTgvVFSOSOmx61C1KMaNsFwM93h-PBdmFm8o45nxDabx48cTbGl4hHuhasjSwPtxPvAV1A7yQMukREERR-nxL8j-EbWYQ8sj4joABQQmjQhkjLFCKSAo4QoxYiQwQhgmkGjCKGAIMMA4BIwQwjhAFMBUCCUAYEIxpYxUCDlEjJYOScSMgsIIAgADwjKEFBAUCkMEMYAagoARzAAHCDCIISKANkgYYBiQwgDDjHEMIGWZFUBQLhgohBGkhECOMEAMIYghogTgQghgiSLCYUegAsJApIQjxABNDFWCa6AIAQ4Q4KgAgIABgGDCMNGIMgQJRQAQTACpgBNIJkUcBMkpoKAgXCjAgAAGKIcYIVAYbZgwggkEmKLEiYGYAYQQShFAAAQBFEEAEuEIgwYRQoARnBkAmAGMEAGFGIgQBigCwAkABEIA'
TEST_2_FP_RAW = [-772063964, -772066012, -1007079116, -1011011276, -1027788492, -1029889740, -1031261916, -1031269084, -1031270620, -1031021744, -1031079600, -1031078425, -1031032346, -1018580506, -1018646290, -1022775046, -1056337446, -1056261686, -1073039030, -1073039013, -1068976005, -1001867175, -733365175, -733302711, -737435575, -603332504, -603365272, -737516311, -188076117, -175490390, -745993558, -758642022, -767030630, -1034347878, -1038412133, -1039584631, -1039654264, -1034345784, -1030086056, -1011141092, -1045873092, -1045939676, -1045947803, -2132276505, -2132259914, -2140415082, -2140472938, -2140481130, -2140546634, -2140603929, -2144802523, -2144536267, -2123540203, -2115147515, -2081855203, -2098598611, -2098606801, -2098606737, -2106995329, -2090217989, -2123638309, -2140477173, -2140477173, -2123634405, -2106992325, -2107061957, -2107061991, -2107007715, -1033140963, -1023769329, -1025864433, -1026913002, -1010133962, -1017409482, -1017540482, -1022848902, -1056337830, -1056271030, -1056261302, -1073038501, -1068975271, -1060587447, -993477559, -1001672631, -737435575, -737566615, -737550231, -737419031, 1422585259, 1955228586, 1367940010, 1388841914, 1380453258, 1376328586, 1376458634, 1107956618, 1107899017, 1113072281, 1121657497, 1119494811, 1135224479, 1135226615, 1139489511, 1130891874, 1126713938, 1109977859, 1114237187, 1122691331, 1122695431, 1122687255, 1114233125, 1130944869, 1126746469, 1097554247, 1105885511, 1105885511, 1135270230, 1122523494, 1114135910, 1109939695, 1093236223, 1076520335, 1080714635, 1089107851, 11092923, 11010986, 15209450, 15492074, 7103274, 2913082, 2905882, 2940681, 2947848, 7138056, 32303368, 61716744, 44932552, 1118668232, 1118406137, 1122600424, 1110167912, 1110167848, 1110106424, 1122689305, 1118495003, 1118478714, 1118540010, 1122599146, 1110016234, 1110147562, 1110094153, 1076535560, 1076538376, -1058363384, -794183656, -794249176, -790063064, -261519320, -261519319, -529562582, -529628886, -530153430, -530280406, -534465494, -534459350, -517027794, -517027778, -517056387, 1630428508, 1634606924, 1643060940, -508616995, -508740929, -475252054, -487834709, -496223301, -496231493, -496092485, -488752486, -489735542, -494125366, -494125542, 1641889598, 1627335998, 1617898782, 1613703454, 1614756622, 537664270, 541854222, 541854238, 541874782, 558651982, 558168910, 558168910, 558168398, 566360398, 1636039038, 1669593454, 1938028670, 1942087766, 1942087766, 1665394807, 1631779173, 1640192868, 1640221300, 1640483428, 1640487796, 1631902020, 1627682884, 553932868, 554654068, 554589029, 567179879, 562985575, 562846279, 562879301, 558684487, 554678646, 554678646, 558873462, 567262070, 563067366, 562936022, 567064775, 558692565, 1628436725, 1661925605, 1661893095, 1666087909, 592329573, 567032663, 567032133, 567032132, 1640840020, 1909340900, 1909340900, -238142748, -775079212, -775152956, -1043580220, -1047774524, -2121450764, -2138162460, -2138162460, -2138232091, -2121520409, -2117330313, -2124670345, -2124604585, -2092205227, -2083848891, -2083787451, -2117489195, -2117550619, -2124902943, -2139517453, -2139383405, -2122597997, -2122598221, -2093090639, -2095162991, -2107737727, -2107754111, -2108805231, -2099495199, -2099499291, -2097402137, -2098451465, -2098709513, -2098717737, -2081859113, -2123773481, -2140434985, -2140496425, -2140428906, -2132171338, -2132236874, -2065124170, -2023181130, -2039964482, -2044162882, -2044098306, -2111137761, -2111117043, -2111165684, -2144720372, -2140460532, -2132132340, -2136328643, -2136407507, -2136471761, -2136471761, -2132277457, -2114187977, -2091268651, -2083809851, -2083872379, -2117361257, -2117552729, -2141681241, -2139584009, -2143708937, -2143618857, -2126874411, -2126894891, -2093339196, -2105923644, -2099628348, -2103836012, -2103966047, -2099751259, -2097639449, -2031579161, -2039763466, -2031375914, -2014728234, -2056675370, -2056548654, -2073127278, -2077251950, -2077233262, -2077266510, -2077332302, -2073154382, -2014434126, -2031143722, -2039794617, -2039792379, -2039792868, -2107033028, -2081936836, -2136462820, -2136265204, -2136263155, -2136456385, -2136456401, -2132228626, -2122791506, -2091070041, -2107647561, -2108769915, -2100384379]

# MP3, 320kbps
TEST_1A_LENGTH = 260
TEST_1A_FP = 'AQABVkmYaEmkJEsiaGvhH33xXNDyol2Pz-jhW2h1_Bb6w4d2dIbPo8dzVA_Es0E1C9_RCGH1DDmP3hX8DD2-Bdq0ojmPa9CeS_CPdi0-9EFz4bqE02iOQzs6w-fR7-gP9R0ct2ipoEeqD60u5EyFPoSPfjF0NNKOXsMP7TkcMxyq3bjQ_GiP05TQw4d24ejQfDl-VD7EN8JdtFTQHWH8DN8RPhXsED_6BdoOv0df_IJ2FuZ69MaF5hba47dQ-OihC42MvjmeQPthvSRqaR3-HfUFH33YoC-UHddRWSL6Gr6gHd0DO-i0Hj1-WMJjXAdeqoN5_MfhrbgOVzyeGRfOCpbIauh7IY8evEGYo0_woIePyxDtFTgJt8d96BM64UZ1mLfQFw96-EW77Oh__Eb64WLwz_DxZXgHU6HRfbjQozlxhOfgH_rRHz0D60eF6-gPvw6Ow0-G_tBzNKxy9BZyoWOI5smR78HDQtMP-0X1Pfjwo9GPfslRiHksoVWIo1zRrMtxo-dhkviPwzo0PniDXsdOWGYLHfZ0_Ef_oGcK0aHxB7uIT7BwGeqP1_CmA_9hnDizGSd-WIfXo8c7VDZ8_Hgo_McP_3ha_Cl8utCD4xS8B8LhzUc9tAcabT1-aBXM4xBx2DrywyS-Z_A5XMVhK0f7ICf6wxb048R15BfOI3eHE0F-4AzM5dCNH4cPO-iOD7_QPELf4egDpzp6dM0g2jh-CSdEEj_yHt6O_ijSG8cDmSSMG3cAn-hxaNE0BbeO_tPQH_5RizGeAwWAQgg4hIwwgBkmgGKKAieMAgBYI4ACBAmHqDECSyYAIQIZDY0CQggFnAIIOCSYABg5AZxCCFBjkHJEGACAUgIoh5QwmCkAFBIEAKQsEEgRYYAU2CHrAABEAMuQcBwAwgBDgmIsjUBEKSKEIgAIAQwACgBrLHEYGKEEBMQAg5wBFAAGlEBGKAYEQcwQBACkigABjBNAKEEAtYIIYhwBgBAjABCSGMEUMIIJZ6QwnFgGJUDCACKYIEBRRcRAACBIrqECOCGtcEwRZpgEijiGjDKCSsYcIApAwQwimDlhhRHGMaGceFZwBxwhDAjCCA'
TEST_1A_FP_RAW = [-1124735545, -1124600491, -1107954315, -1108017819, -1082858139, -1084889769, -1101531321, -1105799353, -1105832105, -1084795017, -1082696345, -1107993113, -1124772361, -1124739625, -1124608571, -1124600491, -1107962507, -1108028059, -1074469531, -1099635403, -1105857257, -1105758393, -1089054905, -1089054729, -1116316186, -1107866137, -1128970761, -1129024041, -1124829753, -1124735033, -1124600491, -1107962523, -1108017819, -1084955273, -1101666985, -1105725625, -1105799353, -1105766569, -1084795033, -1107862169, -1107995161, -1124772393, -1124739625, -1124608571, -1124600491, -1107962507, -1074465435, -1082858123, -1101667017, -1105726121, -1105832121, -1089054889, -1118414858, -1107927578, -1128968729, -1129032201, -1129024041, -1124735545, -1124735035, -1107954315, -1108026011, -1074463387, -1082858121, -1101531881, -1105791161, -1105832121, -1088989321, -1084795545, -1107993113, -1107995145, -1124772393, -1124608571, -1124600379, -1124600491, -1108028059, -1074465435, -1082858187, -1105861353, -1105726121, -1105832121, -1089054761, -1116315674, -1107931674, -1128968713, -1129032233, -1124829737, -1124735545, -1124604587, -1107954315, -1108017819, -1082854043, -1084889737, -1101531305, -1105791161, -1105832121, -1084795017, -1082698393, -1107995161, -1107995145, -1124772393, -1124641337, -1124600379, -1124608651, -1108026011, -1108023963, -1116445321, -1621793321, -1659424313, -1793715833, -1806297705, -1797909065, -1799942745, -1800069705, -1800135279, -1795934831, -1796905535, -1805158959, -1805257231, -1805255197, -1780089485, -1780095661, -1746405437, -1754794029, -1771579437, -1771580045, -1755196045, -1759414925, -1759414925, -1788609229, -1788674285, -1780220397, -1780351469, -1780418765, -1746884813, -1763593453, -1771842797, -1774988525, -1775151277, -1619823117, -1787658781, -1796006430, -1795879454, -1795945005, -1795916349, -1795719741, -1804108333, -1787331085, -1779040781, -1746405935, -1746405935, -1746544687, -1754967055, -1788585999, -1788774413, -1788775069, -1788641949, -1788609229, -1746796781, -1746669821, -1746667773, -1746675949, -1746811085, -1755253469, -1619991245, -1624119501, -1624148206, -1623761134, -1619624110, -1611235470, -1611182734, -1649062542, -1644931246, -1644341310, -1644300350, -1652688942, -1652758558, -1652759070, -1653213709, -1619528237, -1611205167, -1619601983, -1619567151, -1888133775, -1888133855, -1921647327, -1653213903, -1661475567, -1661475503, -1661471407, -1661631119, -1644919455, -1653295773, -1619527853, -1640564925, -1640605886, -1640542254, -1636352030, -1611190813, -1615520285, -1649140303, -1779165807, -1804257855, -1804110399, -2072611391, -2064157327, -2047548063, -2047548047, -1887967981, -1888026877, -1888035069, -1887971821, -1921714397, -1921718429, -1653213325, -1653090989, -1644767789, -1644702253, -1611147917, -1611344799, -1611352735, -1619729039, -1619659403, -1757948459, -1757981225, -1791615497, -1787413065, -1795809881, -1800073801, -1795943019, -1795918379, -1795857967, -1797135919, -1797136015, -1797200783, -1780358093, -1788611533, -1755063021, -1755063021, -1771905709, -1771905677, -1771844237, -1754835469, -1754958349, -1788512269, -1788479661, -1780099469, -1746545053, -1746602141, -1746868429, -1755257069, -1621035245, -1624148205, -1657571501, -1657637549, -1653459597, -1644821133, -1649080845, -1779165741, -1779141167, -1779075631, -1778909743, -1779303183, -1779303181, -1787691789, -1754008109, -1754017341, -1755065389, -1755065389, -1788348573, -1788479709, -1788478159, -1805254895, -1788477679, -1788477645, -1788346573, -1779968237, -1746544878, -1746537166, -1637484686, -1636313262, -1640671406, -1640540334, -1636352142, -1611186846, -1611326109, -1644946061, -1644939949, -1661700783, -1661639343, -1644698287, -1655179952, -581577392, -552084143, -552075439, -552075440, -547885231, -547885231, -547883055, -1621637647, -1613380109, -1646930445, -1646922253, -1646926381, -1646920205, -1646985885, -1647004317, -1653295837, -1653222125, -1623730941, -1623730429, -1623828717, -1619624077, -1611235485, -1611182093, -1611315247, -1611311151, -1655343151, -1653114927, -1653123597, -1653254797, -1644858254, -1611301550, -1644724926, -1644724910, -1653244557, -1653252749, -1661641357, -1661086223, -1661086255, -1661602351, -1653082671, -1653082671, -1653221903, -1619667487, -1619659295, -1619828397, -1888276205, -986509053, -1003417325, -999214797, -990763741, -994962141]

# WMA, 160kbps
TEST_1B_LENGTH = TEST_1A_LENGTH
TEST_1B_FP = 'AQABVkmYaEmkJEsiaDv8Hr0GXRd6FuZ69DP6wBdaHb-FHj60CzeaH33wHNUD8WxQPTiF7ghDPcN5hHcFP0OPb4HWFY3M4xr0XGjeoV2LD33QPMKP_2iOQzs6w-fRa-hz4R_EmClaKjjCCK2eCDkt9GHgo18MoVF79At-aD-cd6g2prjQHw2P05TQw4d2AZ3h8-i1o2oO_1BdBi0V9Ej1DK1y5KnQh_CPfoF2WO3Ra_gF7TnMMUdvXGhuoT1OW-jho4cudEbj5ngCbT_8kri0DtV31Bd8oc_RM1B2XEdliegNf0Ih80HjoNOP_vhh4j-uEXipDuZx_IG34jpc8XhmXMVZwSSPjvWQ5xnOoLkQXviCHj4uQ7SP4xl8GT_0ohOO6oJ5C33xoIdftOPR58dvpB8uBv8MH1_wdLCkEP2GCz18tEf4w8-hox965rB-VLiO_vDr4Dj8DD2P59By5WhvIRc6hmie49ODPCw0_bBfVA8eBUf3F_6SExDzS0GrMDjKFV55VObREyaJ_zisQ-ODN-h17IT1Frpg9_hzoT96BnYI9cEu4hMs_FDp4zW86cCPwyfObMaJH9bh9dAOvUN1-MePh8J_HGZJPMefwqfxHDpOwXsgXPBm1EN7wHKP-tA04YchHoetIz98_Bl8Dj9gK0f7ICf644L448R15BfOIy8uHUF-4AzM5dCNH4cPO-iOD7_QPELf4egDpzp6dM0g2jh-CSdEEj_yHt6O_ihyw8cDmYePG3cAH_1xaJsGx1qOfkXPD_7R17hoAAMAMEYAgqgRBmAkBFJMUWAMNQwAYA1QBiGHpHHCCCyZAAAgAMlRQAhAnBLIOCWYABgJAAhCQjskgSCCAeAMIEA5pATATAElBEIAKQmMQIowoIQQyCFhgANAFMGQcBwARhgSDmMpuDEIKkWEUAQAAYABQAFgDVUOAyAAEp4AYJAzgALAhBDMEAEYIIYoQxB1lAAADHBCCUGAKYIIYowiAAhiBBCSCMEUMCQIZ6QwHCiAGJQACcqMIMAxqIhIABiIraFCACokEI4poohhEijiGDVKGUElYw4QBaBgBhHMnLDCCOOYoEIM46xgwhlLgCACAQ'
TEST_1B_FP_RAW = [-1124735545, -1124604587, -1107954315, -1108026011, -1082854041, -1084889737, -1101531305, -1105799353, -1105766569, -1084795017, -1082696345, -1107993113, -1107995145, -1124772393, -1124608571, -1124600507, -1107831435, -1108028059, -1074469531, -1099635403, -1105857257, -1105791673, -1105832121, -1089054761, -1116316186, -1107866138, -1128970761, -1129024041, -1124829753, -1124735033, -1124600363, -1107962523, -1108017819, -1082858137, -1101666985, -1105725625, -1105799353, -1105766569, -1082697881, -1074309785, -1107995161, -1124772393, -1124739625, -1124608571, -1124600491, -1107962507, -1108017819, -1082858123, -1101732555, -1105726121, -1105832121, -1089054905, -1089054730, -1107927578, -1128837657, -1129032201, -1129024041, -1124735545, -1124735547, -1107823243, -1108028059, -1074465435, -1082858121, -1101667049, -1105791161, -1105832121, -1088989353, -1084795545, -1107993113, -1107995145, -1124772393, -1124608571, -1124608571, -1124600491, -1107962507, -1074463387, -1082858187, -1099569899, -1105726121, -1105832121, -1089054889, -1116317706, -1107931674, -1128968729, -1129032201, -1124829737, -1124735545, -1124604459, -1107954315, -1108026011, -1082851995, -1084955273, -1101531305, -1105791161, -1105832121, -1084795017, -1082698393, -1107993113, -1107995145, -1124772393, -1124641337, -1124600379, -1124608683, -1108026011, -1108023963, -1116445193, -1621793321, -1659424297, -1793715833, -1806297705, -1795811913, -1800008281, -1800069705, -1800135279, -1795934831, -1796905535, -1805163055, -1805257231, -1805257247, -1780089501, -1780095661, -1746409533, -1754794029, -1771579437, -1771579917, -1754933901, -1759414925, -1759414925, -1788609229, -1788674285, -1780285677, -1780351469, -1780418765, -1746884813, -1763593453, -1771842797, -1640770797, -1640933549, -1624017549, -1653441053, -1796071966, -1796141598, -1795945006, -1795924541, -1795719741, -1804108333, -1787331085, -1779040781, -1745357359, -1746405935, -1746414639, -1754967055, -1788520463, -1788774413, -1788775069, -1788773021, -1788609229, -1746796781, -1746669821, -1746667773, -1746675949, -1746811085, -1755261661, -1619991245, -1624119501, -1624148206, -1623761134, -1619624110, -1611235470, -1611248270, -1649062542, -1649125422, -1644341310, -1644300350, -1652688942, -1652693006, -1652759070, -1653279245, -1619528237, -1611139631, -1611213375, -1619567151, -1888133775, -1888133855, -1921647327, -1653213903, -1661475567, -1661475503, -1661471407, -1661627023, -1644919455, -1653295775, -1619528365, -1640564925, -1640605886, -1640542254, -1636335646, -1611190814, -1615520285, -1649140303, -1779165807, -1804331583, -1804110399, -1804175935, -2064157359, -1779112591, -1779112591, -1888099053, -1888026877, -1888035069, -1887971821, -1921648845, -1653282973, -1653213325, -1653090989, -1644767789, -1611213357, -1611147917, -1611344799, -1611352735, -1619729039, -1619659403, -1757940267, -1757981225, -1791599113, -1804190281, -1795809881, -1795879497, -1795943017, -1795918379, -1795857967, -1797135919, -1797136015, -1797201807, -1780358093, -1788611533, -1755063021, -1755063021, -1755128493, -1771905709, -1771844237, -1754835469, -1754958349, -1788512269, -1788479661, -1780099469, -1746545055, -1746602141, -1746864333, -1755257069, -1621035245, -1624148205, -1657571501, -1657637037, -1653197453, -1644821133, -1649080845, -1644948013, -1779141165, -1779075631, -1778909743, -1779303183, -1779303181, -1754137357, -1754008109, -1754017341, -1755065389, -1755065389, -1788349581, -1788479645, -1788478159, -1805254863, -1805254895, -1788477645, -1788346573, -1779968237, -1746544878, -1746536654, -1637484686, -1636313262, -1640540334, -1640540334, -1636352142, -1611186846, -1611326109, -1644946061, -1644939917, -1661700783, -1661639343, -1644698287, -1655179952, -581577392, -585640623, -552075439, -552075440, -547885231, -547885231, -547883055, -1621637647, -1613380109, -1646930445, -1646922253, -1646926381, -1646920205, -1646985885, -1647004317, -1653295837, -1653222125, -1623730941, -1623730429, -1623828717, -1619624077, -1611235485, -1611182093, -1611315247, -1611311151, -1655343151, -1653114927, -1653123597, -1653254797, -1644858254, -1611301550, -1644724926, -1644724910, -1653244589, -1653252749, -1661641357, -1661118991, -1661086255, -1661602351, -1653082671, -1653082671, -1653090831, -1619667487, -1619659295, -1619697293, -1888276205, -852283133, -1003417325, -999214797, -990699229, -994953949]

# Vorbis, 64kbps
TEST_1C_LENGTH = TEST_1A_LENGTH
TEST_1C_FP = 'AQABYpESSUkiJYmSCD30C81RbeXwG7zQvBFa4bfQg_rRQ5vh8-jxHJoe-AyD6sF5NEJYPUPOo3cFP0N7fCm0F40k8fgOPUfzo12LDz0a3sIv4TSa44KGDv7Ra-hz4e8gxi1aBz8aHWF1CXlooWfgg_mO9hDVg6nwQ3sOnx2YvriC_mioBxc6Gj566ASzwyf6Hf0h5h3uFqeCw5I-9Bf6VLBD_OgXaD0srRz64tB-wdmYozp6IX2EVsgtdISPHjoaHX3woPshviQurUP1HfUFH30b9LCLH5oscXgx5YJ2dIedo12P7vhh3MJ9nHipDuZx_IG34jpcEc8cXMVZwRJZoe_xsMGZo3ExXbgWFNsf6Bvs43gG3_ihr-g0vCl6mLfQFw_RD36PdjzRLid848PF4J_h48uQv4OpEP2GS-gNn2gRnsN_iPvRC_1hyUL1D5eOwn9w3PCJXof2w1eO9hZyoWPRPEe-Bw8LTT_so_oefMePRj_6JUcPMW0stCOOckWzLsd99IRJCh9x-OgDPeh17IQos_jhtMdzoT-0M7BD_MFF7BNh4Tp0HTe86Tj-4_CJM5txwjxuCcp2lMe-Q5MN8_g-PMZ_HOaJJ8efwqeh5zhOwTt0XPBm1EN7oNHW4zu04zAMHbYuHOmP34F_XMUJ_2j14CHCh4cPXcdxHXmp48iPXDqOHDgDc4FuFcdh2OguPLgvNI_wdyj6wKmOHl0ziDZ-_NApWCKB_IKHcsYR3vDxBzoJ48YdwOdRHFq04l-Ofuj5Df5RizGeC-FD-AkeTLrxJsePUP1x7dCxc0Z8-DvCdcEvAIUQAsYgYYAhTADFFAXEIKMAAIwJ4IBhSDgElBFYKgAAAsYhaJAQAgBFCUBAOCWMyEhRQYhABhiSBFGOCKHMIEASSTFzVDEhEAJIWcAcYQZQJKRDRiAMgCiCIccBII4ZoYyQzholDQFICEUAAAAxBYA1wCjHgCBECAAUIMZAgCwQRhBDBGBCEMQMQQBAQxUBAoAngBTUJKUEMVIRJ4gRACAGJFFWOWCEA8JJAQki1ggJkKCEEUGAYlQRKhIAAhhprHAACSAdEYoBIphgEijgqCAELCGZAwoQYQQimDEnJDOmCSGNs0I4IIwlQBAGAGJGEEkAYEAJIASgAA'
TEST_1C_FP_RAW = [-1107954315, -1108019867, -1082858137, -1082792617, -1101531385, -1105791161, -1105832113, -1082697857, -1082696337, -1107993105, -1107995137, -1124739625, -1124608569, -1124600491, -1107962507, -1108028059, -1074469531, -1099635401, -1105726185, -1105824441, -1089054905, -1089054729, -1116316186, -1107866137, -1128970761, -1129024041, -1124829241, -1126832185, -1126697003, -1110057627, -1118503579, -1084955289, -1101666985, -1105725625, -1105799353, -1105832105, -1084795545, -1107862169, -1107995161, -1124772393, -1124608553, -1124608571, -1124608683, -1107962507, -1108017819, -1082858123, -1101667019, -1105726121, -1105823929, -1089054905, -1084860425, -1107927578, -1128839705, -1129032201, -1129024041, -1124801073, -1124735009, -1107953795, -1107952283, -1074463387, -1082858121, -1101662889, -1105725617, -1105832113, -1088989345, -1082696337, -1107862161, -1107995137, -1124772385, -1124739633, -1124600371, -1107823275, -1107962507, -1074465435, -1082858123, -1101667049, -1105726121, -1105832105, -1089054889, -1118413321, -1107931673, -1128968713, -1129032233, -1124829737, -1124735545, -1124603947, -1110051467, -1108019867, -1074465435, -1084955273, -1101531369, -1105725625, -1105766569, -1082697866, -1082696346, -1107993241, -1107995145, -1124772393, -1124641337, -1124608571, -1107831435, -1108028059, -1108023963, -1116445195, -1621793321, -1659424297, -1793715833, -1806297705, -1797909065, -1799938649, -1800069705, -1800137321, -1795934825, -1805294139, -1805158971, -1805257231, -1805255197, -1788478093, -1780095661, -1746405565, -1754794029, -1771579437, -1771579405, -1771743757, -1754958477, -1759414925, -1788609229, -1788674285, -1780285677, -1780351469, -1780418765, -1746884813, -1746816237, -1771842797, -1640770797, -1640933549, -1619823117, -1653441053, -1661592093, -1795879453, -1795947053, -1795926585, -1795719737, -1795719721, -1787298317, -1780089359, -1746537007, -1746405935, -1746414639, -1754934287, -1788521487, -1788774413, -1788779165, -1788642013, -1788609229, -1746796781, -1746669821, -1746733309, -1746675949, -1763588301, -1637821149, -1619990733, -1624119533, -1624148205, -1623761133, -1619624109, -1611235469, -1611182733, -1649062414, -1649125422, -1644341310, -1644169278, -1652688942, -1652758542, -1652759070, -1653213709, -1619528461, -1611205167, -1611211327, -1619534383, -1619697807, -1921655007, -1653213919, -1653213903, -1661606639, -1661475567, -1661471407, -1661610639, -1644915359, -1653295757, -1619528365, -1640564925, -1640605886, -1640538158, -1636352030, -1611190813, -1615520285, -1649140303, -1644948079, -1670040127, -1804110399, -2072611391, -2064157327, -2047548063, -1913330319, -1887965933, -1888026877, -1888035069, -1887971821, -1921714397, -1653282973, -1653213325, -1652566701, -1644767917, -1611213485, -1611147917, -1611344541, -1611352735, -1619729039, -1619659403, -1623730729, -1757981225, -1791599177, -1804190281, -1795809881, -1795879499, -1795943019, -1795918379, -1795857963, -1780358703, -1780358799, -1797136335, -1780353997, -1788611533, -1755063021, -1755054829, -1771897517, -1771905709, -1771844237, -1754835469, -1754958349, -1788512301, -1788356781, -1779968395, -1780099227, -1746602143, -1746868429, -1612651245, -1619986669, -1624148205, -1657571501, -1657637037, -1653181069, -1644821133, -1649080845, -1644948013, -1779141167, -1779075631, -1778909743, -1779041039, -1779303181, -1754137357, -1754008109, -1754017341, -1755065389, -1755065389, -1788348573, -1788480221, -1788478159, -1788477647, -1788477679, -1788477647, -1788346573, -1746413805, -1746544877, -1612318926, -1637353614, -1636313262, -1640671406, -1640532142, -1636354190, -1611186846, -1611330206, -1644948109, -1644939949, -1661635247, -1661639343, -1644698287, -581569200, -581577392, -547891887, -552075440, -547881136, -547885231, -547885231, -547883055, -547895823, -1646934541, -1646930445, -1646922253, -1646922285, -1646920205, -1647002269, -1647008413, -1653295837, -1653222125, -1623730413, -1623730429, -1623828717, -1619624077, -1611235485, -1611182093, -1611315247, -1644865583, -1646954543, -1653114925, -1653254797, -1653254797, -1611303566, -1611303854, -1611170494, -1644724926, -1653244589, -1653252749, -1661641229, -1661086223, -1661086255, -1661602351, -1653082671, -1653082671, -1619667471, -1619667487, -1619659295, -1619693229, -1888276205, -1926024957, -1003417325, -999214797, -990763741, -996010717, -995947214, -995881710, -995869422, -991609530, -999993914, -983183930, -949893737, -966552169, -966543979, -958271087, -958279216, -941559312, -941530783, -983473887]

# WMA, 32kbps
TEST_1D_LENGTH = TEST_1A_LENGTH
TEST_1D_FP = 'AQABVkmYaEkkZUkE7bDao4e-C9VhHtWLHtQFphJ-CT3sQ7vQGT76Bc_RB-LZ4Bb6HR3CUB9yVugr2MnQH_qITieah8eL_oIYs8O3FkUvNK6Fv0L3wz4O7egMn0e_oz_UD45pnBJ-pPLRShdyFn1awZ9xfIQorUdPfIf2C455tC-OXhcaqngldId99IKODs2X40d_OG8E1UXrox9SSR_6C3kq9CH8o1-gHVaPfsUvaD-cjTmq40JjXQjLIxc6Gj56XNAi9MvxBtotwSe-FtVP9BZ89HnQB3aIHz2Jn0Vz9DyOxjmm3sKPHy189MdR7R1s_PBRrofWHmL94Bl-4azQyDzySR725MGZojn65MiJ32g-6Me2_fjxDL7xHM_moWunQzVaUYePkniPcjr8oucR_vCP7_jxJsR_mAv-dIIdyWiPoz_RPPiQH_2h5ceLe0dzVDe-oRfSuA5w-BnC83gOLVc6hP1xoWPRPMf3DHlYNDEPPUf_4Ffwo_mDrkugwXmMVuFxlOvhdUGPmzu0koePH97RB3M__OglwzLxQ_SO6rPwoyfsMHhxSjiPY1Nw6sFhGzmQ74aD91Cm48R9eLfQ4x2gaTv8o9qN6-hhHk-OzylOuMuh4xSMH_phH6VGoEWjFyd2QouFAzquw3yOHM6-BdeL4_AZon_wZTm60sgvGLqE_0beEaeL_BtO_Phx4xrhBz9eEuKD5xDRszNOqEcfHeaL8OhVOKbRH-G0TDC1FdczHDd-I5WOw84u_MKRGz70bDhTIe_hGzcOoz9yaFsVw_mFfuh5pD96xrhyAAaIAgYiRIVjDGHCFAaGCKQYAkIAQIkBxAAjmGQCECIQNFQQo4CQBhBHBBECEEANQ0oApwQyhCBBJBBEUEWcEQRIRwTIzBEgEIBAKQuIckQAAQAUSjDljCKEDAIVkcAZBAAhhiEhFCFAIQWcMko6I4RlgAIBCACGKSoUEEQQ4AQwBgsFlFACKAkCE0IwQ4BwQhikiDHEAEEdAoY4IoBgFiKkEENCEgScEQ5QIwEipAkljBGKMIKAAFIoxohgAipClHEMICyVEYAJBywUChjBCDICAIeEs4gZJQAFTCglBCVEICAQA846IZywglHhhTLCkibQEJwAQQQiAA'
TEST_1D_FP_RAW = [-1126832697, -1126701611, -1110051467, -1110059675, -1084951193, -1084885705, -1101662441, -1105725625, -1105758377, -1084786817, -1084793497, -1107862041, -1107993097, -1124772393, -1124608571, -1124600491, -1107823243, -1108028059, -1074469531, -1099635339, -1105857193, -1105758377, -1089054905, -1089054761, -1118413338, -1107866137, -1128968713, -1129024041, -1124796985, -1124735035, -1126701739, -1110059675, -1108028059, -1082854027, -1101667049, -1105725609, -1105725625, -1105766569, -1084858521, -1074307737, -1107993097, -1124772393, -1124739625, -1124608571, -1124600491, -1107962507, -1074465435, -1082858123, -1101732553, -1105857193, -1105766569, -1089054889, -1084852234, -1110024730, -1107866137, -1128966665, -1124829737, -1124796969, -1124735017, -1107823243, -1107962523, -1074465435, -1084955273, -1101662953, -1105725689, -1105725625, -1084795049, -1084859033, -1107862169, -1107993097, -1124772393, -1124608569, -1124600379, -1124600491, -1108028059, -1074465435, -1082858123, -1105861355, -1105726121, -1088981177, -1089054889, -1118413322, -1107931674, -1128968729, -1129032201, -1124829737, -1124735545, -1126832683, -1110051467, -1108028059, -1082854043, -1084955273, -1101531369, -1105725625, -1105766585, -1084784777, -1082696346, -1107862169, -1107995145, -1124772393, -1124641337, -1124600377, -1124600459, -1108028059, -1108023835, -1084987913, -1084918313, -1223215657, -1793649273, -1806297705, -1797909065, -1800008281, -1800073801, -1800137321, -1795934825, -1796921977, -1805556281, -1805552137, -731775513, -731775641, -715004585, -672929981, -689703101, -698099901, -698100397, -698231437, -702417565, -685640349, -714868941, -714866925, -706478573, -706609613, -673122525, -1746881231, -1771982573, -1771843309, -1774988525, -1775151277, -1758234653, -1787681310, -1796071962, -1800335898, -1800401450, -1796178490, -1796117049, -1804374841, -1804337929, -1787568907, -705440303, -671877679, -671886383, -680406031, -1754246159, -1791920655, -714906271, -714902237, -681443533, -673054957, -673059325, -689701373, -1763453165, -1763588301, -1772038365, -1770981582, -1775180014, -1640990958, -1624148206, -1619624174, -1611251886, -1611264654, -1783296526, -1779149358, -1779083326, -1779075134, -1786943534, -1786976286, -1786972702, -1653279261, -1644825101, -1611139647, -1611203135, -1619534527, -1619665551, -1892295391, -1653220063, -1653213903, -1661475504, -1661475504, -1661471408, -1661627024, -1644919455, -1653295775, -1623722669, -1640564926, -1640605886, -1640538158, -1636352030, -1745408542, -1749738013, -1783362157, -1779165807, -1804323455, -1804110399, -730434111, -705202703, -705370783, -705370765, -713562861, -680067325, -680075517, -713566701, -713754829, -713758941, -578947229, -1652566671, -1644178095, -1610640047, -1611164559, -1611361183, -1762347675, -1770740379, -1774848651, -1774725675, -1757981227, -1791549961, -1804190297, -1795809881, -1795748425, -1795943017, -1796196969, -1796185641, -723426857, -723394089, -723394445, -715000781, -715000525, -714867437, -681313006, -681313006, -1771905773, -1771905677, -1755064973, -1755195947, -1755187243, -1788749995, -1746676107, -1746807195, -1746864283, -1746864283, -1755257545, -1754204905, -1758333113, -1791789241, -1791854761, -1787660937, -1779301001, -1783561737, -1783623177, -1779403305, -1779337771, -1779171883, -1779171851, -1779303179, -1787699977, -1754147625, -1754009145, -1754009145, -1754008617, -1788611737, -1788610777, -1788750045, -1788739823, -1788477679, -1788477679, -1788346605, -1779968237, -1746807501, -1746799310, -1770784942, -1640802478, -1640933550, -1640949934, -1636354190, -1611253918, -1644886686, -1649142286, -1661717005, -1661717037, -1661639215, -570988591, -570427568, -847390896, -818553007, -818413743, -550109359, -545919151, -545790127, -545851951, -545864207, -537410063, -573188623, -573196845, -589976109, -589976079, -1644904991, -1644907167, -1653295837, -1619667661, -1623730413, -1623763198, -1624015086, -1619890318, -1611497630, -1611182605, -1615525933, -1646962733, -1646954541, -1655212077, -1787340845, -1787472526, -1787464334, -1745490606, -1644696238, -1644692142, -1653211821, -1653219981, -722084495, -721435151, -587344400, -587860528, -596118064, -579340848, -579340816, -545917472, -680135199, -697077389, -684510957, -986500861, -1003417325, -999214798, -990764766, -994962142]

TEST_1_LENGTH = TEST_1A_LENGTH
TEST_1_FP = TEST_1A_FP
TEST_1_FP_RAW = TEST_1A_FP_RAW

script = None

SEQUENCES = [
    ('account', 'id'),
    ('application', 'id'),
    ('format', 'id'),
    ('foreignid', 'id'),
    ('foreignid_vendor', 'id'),
    ('source', 'id'),
    ('submission', 'id'),
    ('track', 'id'),
    ('track_mbid', 'id'),
    ('track_mbid_source', 'id'),
    ('track_mbid_change', 'id'),
    ('track_mbid_flag', 'id'),
    ('track_puid', 'id'),
    ('track_puid_source', 'id'),
    ('track_meta', 'id'),
    ('track_meta_source', 'id'),
    ('track_foreignid', 'id'),
    ('track_foreignid_source', 'id'),
    ('fingerprint', 'id'),
    ('fingerprint_source', 'id'),
    ('meta', 'id'),
]

TABLES = [
    'account',
    'application',
    'format',
    'foreignid',
    'foreignid_vendor',
    'source',
    'stats',
    'track',
    'track_mbid',
    'track_mbid_source',
    'track_mbid_change',
    'track_mbid_flag',
    'track_puid',
    'track_puid_source',
    'track_meta',
    'track_meta_source',
    'track_foreignid',
    'track_foreignid_source',
    'meta',
    'musicbrainz.artist_credit_name',
    'musicbrainz.artist_credit',
    'musicbrainz.artist_name',
    'musicbrainz.artist',
    'musicbrainz.track_name',
    'musicbrainz.track',
    'musicbrainz.release',
    'musicbrainz.medium',
    'musicbrainz.medium_format',
    'musicbrainz.recording',
    'musicbrainz.release_name',
    'musicbrainz.release_group',
    'musicbrainz.clientversion',
    'musicbrainz.tracklist',
]

BASE_SQL = '''
INSERT INTO account (name, apikey, lastlogin) VALUES ('User 1', 'user1key', now() - INTERVAL '2 day');
INSERT INTO account (name, apikey, lastlogin) VALUES ('User 2', 'user2key', now() - INTERVAL '5 day');
INSERT INTO application (name, apikey, version, account_id) VALUES ('App 1', 'app1key', '0.1', 1);
INSERT INTO application (name, apikey, version, account_id) VALUES ('App 2', 'app2key', '0.1', 2);
INSERT INTO format (name) VALUES ('FLAC');
INSERT INTO source (account_id, application_id) VALUES (1, 1);
INSERT INTO source (account_id, application_id) VALUES (2, 2);
INSERT INTO track (id, gid) VALUES
    (1, 'eb31d1c3-950e-468b-9e36-e46fa75b1291'),
    (2, '92732e4b-97c6-4250-b237-1636384d466f'),
    (3, '30e66c45-f761-490a-b1bd-55763e8b59be'),
    (4, '014e973b-368e-42bf-b619-84cab14c4af6');
INSERT INTO track_mbid (track_id, mbid, submission_count) VALUES (1, 'b81f83ee-4da4-11e0-9ed8-0025225356f3', 1);
INSERT INTO meta (id, track, artist) VALUES (1, 'Custom Track', 'Custom Artist');
INSERT INTO meta (id, track, artist) VALUES (2, 'Custom Track', 'Custom Artist');
INSERT INTO track_meta (track_id, meta_id, submission_count) VALUES (1, 1, 1);
INSERT INTO track_meta (track_id, meta_id, submission_count) VALUES (1, 2, 10);
'''


def prepare_sequences(conn):
    with conn.begin():
        for table, column in SEQUENCES:
            conn.execute("""
                SELECT setval('%(table)s_%(column)s_seq',
                    coalesce((SELECT max(%(column)s) FROM %(table)s), 0) + 1, false)
            """ % {'table': table, 'column': column})


def prepare_database(conn, sql, params=None):
    with conn.begin():
        prepare_sequences(conn)
        conn.execute(sql, params)
        prepare_sequences(conn)


def with_database(func):
    def wrapper(*args, **kwargs):
        with closing(script.engine.connect()) as conn:
            prepare_sequences(conn)
            trans = conn.begin()
            try:
                func(conn, *args, **kwargs)
            finally:
                trans.rollback()
    wrapper = make_decorator(func)(wrapper)
    return wrapper


def with_database_context(cleanup=False):
    def inner(func):
        def wrapper(*args, **kwargs):
            with DatabaseContext(script) as db:
                prepare_sequences(conn)
                try:
                    func(db, *args, **kwargs)
                finally:
                    if cleanup:
                        pass
        wrapper = make_decorator(func)(wrapper)
        return wrapper
    return inner


def cleanup_database():
    create_all(script.db)


def setup():
    global script
    config_path = os.path.dirname(os.path.abspath(__file__)) + '/../acoustid-test.conf'
    script = Script(config_path, tests=True)
    if not os.environ.get('SKIP_DB_SETUP'):
        with DatabaseContext(script) as db:
            conn = db.session.connection()
            if os.environ.get('ACOUSTID_TEST_FULL_DB_SETUP'):
                conn.execute('CREATE EXTENSION intarray')
                conn.execute('CREATE EXTENSION pgcrypto')
                conn.execute('CREATE EXTENSION cube')
                conn.execute('CREATE EXTENSION acoustid')
            metadata.create_all(conn)
            for table in reversed(metadata.sorted_tables):
                conn.execute(table.delete())
            prepare_database(conn, BASE_SQL)
            db.session.commit()


def make_web_application():
    from acoustid.web.app import make_application
    config_path = os.path.dirname(os.path.abspath(__file__)) + '/../acoustid-test.conf'
    return make_application(config_path, tests=True)


def assert_dict_equals(d1, d2, msg=None):
    if d1 != d2:
        standardMsg = '%s != %s' % (repr(d1), repr(d2))
        diff = ('\n' + '\n'.join(difflib.ndiff(
                       pprint.pformat(d1).splitlines(),
                       pprint.pformat(d2).splitlines())))
        assert d1 == d2, standardMsg + '\n' + diff


def assert_json_equals(expected, actual):
    assert_dict_equals(expected, json.loads(actual))
