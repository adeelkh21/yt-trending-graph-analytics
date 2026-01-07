
# Phase 3: Exploratory Data Analysis (EDA) Report

## Generated: 2025-11-09 15:27:51

---

## 1. Dataset Overview

- **Total Videos**: 50,357
- **Countries**: IN, CA, GB, US
- **Date Range**: 2017-11-14 to 2018-06-14
- **Categories**: 18 unique categories
- **Channels**: 8,053 unique channels

---

## 2. Summary Statistics

### 2.1 Overall Statistics

              views          likes      dislikes  comment_count  engagement_ratio  like_dislike_ratio
count  5.035700e+04   50357.000000  50357.000000   50357.000000      50357.000000        50357.000000
mean   1.064764e+06   28141.033360   1292.613275    3075.684960          0.030344           34.719999
std    3.284276e+06   87971.033944   4451.979285    8819.364273          0.032136           53.200820
min    5.590000e+02       1.000000      1.000000       1.000000          0.000000            0.040000
25%    1.079800e+05    1065.000000     79.000000     157.000000          0.010000            7.220000
50%    2.841630e+05    4395.000000    240.000000     659.000000          0.020000           17.500000
75%    7.769980e+05   17791.000000    776.000000    2175.000000          0.040000           42.630000
max    4.083809e+07  985482.710000  51197.810000   90062.910000          0.500000         2844.330000
mode   4.083809e+07       1.000000      1.000000       1.000000          0.010000            1.000000

### 2.2 Country-wise Statistics

  country  num_videos     avg_views     avg_likes  avg_dislikes  avg_comments  avg_engagement_ratio  avg_like_dislike_ratio  median_views  median_likes     std_views      std_likes  max_views  max_likes
0      US        6351  1.780739e+06  49720.898545   2114.104201   5159.505325              0.033593               41.244935      518107.0       11906.0  4.494866e+06  122707.049851   40838093  985482.71
1      GB        3272  3.426436e+06  82402.006030   3533.954514   7312.672109              0.034615               47.096840      597620.0       13401.0  7.783632e+06  180695.976598   40838093  985482.71
2      CA       24427  8.220426e+05  24660.807783   1084.634052   3121.554999              0.035681               43.660784      287976.0        5536.0  2.234651e+06   70021.130929   40838093  985482.71
3      IN       16307  6.756323e+05  14062.161943    834.487997   1345.248182              0.020225               16.302542      205800.0        1745.0  2.061650e+06   56148.709569   40838093  985482.71

### 2.3 Videos per Country

country
CA    24427
IN    16307
US     6351
GB     3272

---

## 3. Top Categories

### 3.1 Top 5 Categories by Video Count


**US:**
category_name
Entertainment      1621
Music               801
Howto & Style       594
Comedy              544
News & Politics     504


**GB:**
category_name
Music             877
Entertainment     858
People & Blogs    282
Sports            212
Comedy            205


**CA:**
category_name
Entertainment      8245
News & Politics    2940
People & Blogs     2553
Comedy             1947
Sports             1932


**IN:**
category_name
Entertainment      7548
News & Politics    2505
People & Blogs     1232
Music              1213
Comedy             1114


### 3.2 Top 5 Categories by Average Views

**US:**
category_name
Music                    4.877963e+06
Film & Animation         2.535137e+06
Gaming                   2.325087e+06
Nonprofits & Activism    2.218901e+06
Entertainment            1.623093e+06

**GB:**
category_name
Music                   8.236766e+06
Unknown (29)            5.092040e+06
Film & Animation        2.456915e+06
Entertainment           2.334395e+06
Science & Technology    2.039720e+06

**CA:**
category_name
Movies                  5.661965e+06
Music                   3.014884e+06
Film & Animation        9.940670e+05
Science & Technology    9.694193e+05
Comedy                  8.732121e+05

**IN:**
category_name
Movies              3.862190e+06
Gaming              3.436402e+06
Pets & Animals      2.490776e+06
Music               2.015096e+06
Film & Animation    1.803889e+06


---

## 4. Top Channels

### 4.1 Top 10 Channels by Total Views


**US:**
channel_title
Dude Perfect                   206044429
ibighit                        189580577
Ed Sheeran                     152189872
Marvel Entertainment           141620998
jypentertainment               139541200
Universal Pictures             123464870
20th Century Fox               113243673
Sony Pictures Entertainment    112842369
Warner Bros. Pictures          110082156
Jimmy Kimmel Live              101962900


**GB:**
channel_title
ibighit                 201139691
Marvel Entertainment    160915035
jypentertainment        141057307
EminemVEVO              133906951
Cardi B                 127254062
Logan Paul Vlogs        126140360
Ozuna                   124191390
Ed Sheeran              122514279
SMTOWN                  121832143
ChainsmokersVEVO        117144486


**CA:**
channel_title
T-Series                              342015089
MLG Highlights                        199094694
Dude Perfect                          196804885
PewDiePie                             183430917
Speed Records                         165834623
5-Minute Crafts                       164566322
The Late Show with Stephen Colbert    143383184
Marvel Entertainment                  137679657
Troom Troom                           136223064
TheEllenShow                          130682714


**IN:**
channel_title
T-Series                492076875
5-Minute Crafts         207643050
Speed Records           177901300
Zee Music Company       166446038
YRF                     161266199
Dude Perfect            158854120
Amit Bhadana            158724851
PewDiePie               153189628
Marvel Entertainment    146422547
Goldmines Telefilms     146326570


### 4.2 Top 10 Channels by Average Engagement Ratio

**US:**
channel_title
KickThePj         0.190000
Amber Liu         0.180000
Desimpedidos      0.180000
Max Joseph        0.170000
Scotty Sire       0.160000
Smyang Piano      0.150000
Caspar            0.150000
ConnorFranta      0.148333
The Valleyfolk    0.145000
AmazingPhil       0.143333

**GB:**
channel_title
KickThePj         0.186
ConnorFranta      0.180
LukeIsNotSexy     0.180
TopicMusicTV      0.170
official A.C.E    0.160
Mouthy Buddha     0.150
ElleOfTheMills    0.150
AmazingPhil       0.150
NiallHoranVEVO    0.145
infinitehome      0.145

**CA:**
channel_title
Papi Melv         0.29
JaeSix            0.28
starshipTV        0.27
Danny Gonzalez    0.26
Lael Hansen       0.25
official A.C.E    0.24
Studio Killers    0.24
Camila Cuevas     0.23
ImmortalHD        0.22
5SOSVEVO          0.22

**IN:**
channel_title
Prasadtechintelugu         0.216250
The RawKnee Show           0.160000
KhilliBuzzChiru            0.150000
The Bong Guy               0.150000
Captain Nick               0.150000
TG Films                   0.145000
Technical Guruji           0.139640
Sharmaji Technical         0.130227
Dhruv Rathee               0.127500
The Baigan Vines Extras    0.123000


---

## 5. Correlation Analysis

### 5.1 Correlation Matrix

                       views     likes  dislikes  comment_count  engagement_ratio  like_dislike_ratio
views               1.000000  0.835592  0.762561       0.680379         -0.007742           -0.012097
likes               0.835592  1.000000  0.727076       0.849085          0.207634            0.110608
dislikes            0.762561  0.727076  1.000000       0.718700          0.050202           -0.070672
comment_count       0.680379  0.849085  0.718700       1.000000          0.266853            0.081768
engagement_ratio   -0.007742  0.207634  0.050202       0.266853          1.000000            0.574143
like_dislike_ratio -0.012097  0.110608 -0.070672       0.081768          0.574143            1.000000

### 5.2 Key Correlations

- Views vs Likes: 0.836
- Views vs Comments: 0.680
- Views vs Engagement Ratio: -0.008
- Likes vs Engagement Ratio: 0.208

---

## 6. Day-of-Week Patterns

### 6.1 Peak Trending Days

- **US**: Thursday (1197 videos)
- **GB**: Thursday (672 videos)
- **CA**: Tuesday (3719 videos)
- **IN**: Tuesday (2542 videos)

---

## 7. Key Insights

### 7.1 Engagement Patterns

- Average engagement ratio: 0.030
- Average like-dislike ratio: 34.720
- Videos with highest engagement: Xiaomi Redmi 5A Unboxing & initial impressions ll ...

### 7.2 Category Insights

- Most popular category overall: Entertainment
- Category with highest average views: Movies
- Category with highest engagement: Science & Technology

### 7.3 Country Insights

- Country with most videos: CA
- Country with highest average views: GB
- Country with highest engagement: CA

---

## 8. Visualizations Generated

All visualizations have been saved in the `phase3_visualizations` directory:

- Distribution charts (histograms, boxplots)
- Country-wise analysis charts
- Trend analysis charts
- Correlation heatmaps
- Scatter plots
- Channel analysis charts
- Tag analysis charts

---

## 9. Files Generated

1. **phase3_summary_statistics.csv** - Comprehensive summary statistics
2. **phase3_visualizations/** - Directory containing all visualizations
3. **phase3_eda_report.md** - This report

---

**Report Generated**: 2025-11-09 15:27:51
