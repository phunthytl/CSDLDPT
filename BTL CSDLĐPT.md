# **ĐỀ BÀI** 

Xây dựng hệ CSDL lưu trữ và tìm kiếm bản nhạc bằng âm thanh.

1.Hãy xây dựng/sưu tầm một bộ dữ liệu gồm ít nhất 500 files âm thanh ngắn về các bản nhạc không lời, các files có độ dài phù hợp để trích xuất thuộc tính, mỗi file có nội dung về một bản nhạc có giai điệu cụ thể (SV tùy chọn định dạng file âm thanh).

2.Hãy xây dựng một bộ thuộc tính để nhận diện bản nhạc của các file âm thanh có trong bộ dữ liệu đã thu thập (gồm các thuộc tính giúp xác định sự tương đồng và xác định sự khác nhau giữa các đoạn nhạc). Trình bày cụ thể về lý do lựa chọn và giá trị thông tin của các thuộc tính này.

3\. Hãy xây dựng hệ CSDL để quản lý các siêu dữ liệu đã có, trình bày cơ chế tìm kiếm các bản nhạc tương đồng dựa trên bộ siêu dữ liệu này.

4\. Xây dựng hệ thống tìm kiếm file nhạc với đầu vào là một file âm thanh về một đoạn bản nhạc đã có và không có trong dữ liệu, đầu ra là 5 files âm thanh giống nhất, xếp thứ tự giảm dần về độ tương đồng nội dung với file âm thanh đầu vào.

a.Trình bày sơ đồ khối của hệ thống và quy trình thực hiện yêu cầu của đề bài.

b.Trình bày các kết quả trung gian của quá trình tìm kiếm files nhạc tương đồng nói trên.

5\. Demo hệ thống và đánh giá kết quả đã đạt được.

# **PHẦN 1\. GIỚI THIỆU CHUNG**

## **1.1. Mục tiêu**

## **1.2. Bộ dữ liệu**

# **PHẦN 2\. XÂY DỰNG BỘ THUỘC TÍNH NHẬN DIỆN BẢN NHẠC**

## **2.1. Nguyên tắc trích xuất nhiều vector cho file âm thanh 30 giây**

Với file âm thanh dài khoảng 30 giây, nên trích xuất nhiều vector theo từng đoạn ngắn thay vì chỉ trích xuất một vector duy nhất cho toàn bộ file. Lý do là tín hiệu âm nhạc thay đổi liên tục theo thời gian, có thể thay đổi về giai điệu, nhạc cụ, tiết tấu, âm lượng và năng lượng.

Đề xuất chia file bằng cửa sổ trượt: độ dài cửa sổ W \= 5 giây, bước trượt H \= 2,5 giây, độ chồng lấn 50%. Khi đó, một file 30 giây sẽ tạo ra khoảng 11 vector đặc trưng.

**Số vector \= floor((T \- W) / H) \+ 1**

Trong đó: T là thời lượng file âm thanh, W là độ dài cửa sổ, H là bước trượt. Với T \= 30, W \= 5, H \= 2,5 thì số vector \= floor((30 \- 5\) / 2,5) \+ 1 \= 11\.

Cách làm này giúp giữ được thông tin cục bộ của từng đoạn nhạc. Khi file truy vấn chỉ là một đoạn ngắn, hệ thống vẫn có thể so sánh với từng đoạn trong cơ sở dữ liệu để tìm bản nhạc tương đồng nhất.

## **2.2. Thuộc tính trên miền thời gian**

Miền thời gian biểu diễn trực tiếp biên độ tín hiệu âm thanh theo thời gian. Các thuộc tính trong miền này giúp mô tả năng lượng, cường độ, nhịp độ và mức biến động của tín hiệu.

### ***2.2.1. Zero Crossing Rate (ZCR)***

**Khái niệm:** Zero Crossing Rate là tỷ lệ số lần tín hiệu đổi dấu từ dương sang âm hoặc từ âm sang dương trong một khung tín hiệu.

**Công thức:** 

![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>Z\</mi\>\<mi\>C\</mi\>\<mi\>R\</mi\>\<mo\>=\</mo\>\<mfrac\>\<mn\>1\</mn\>\<mrow\>\<mn\>2\</mn\>\<mi\>N\</mi\>\</mrow\>\</mfrac\>\<munderover\>\<mo\>&\#x2211;\</mo\>\<mrow\>\<mi\>n\</mi\>\<mo\>=\</mo\>\<mn\>1\</mn\>\</mrow\>\<mi\>N\</mi\>\</munderover\>\<mfenced open=\\"|\\" close=\\"|\\"\>\<mrow\>\<mo\>sgn\</mo\>\<mo\>(\</mo\>\<mi\>x\</mi\>\<mo\>\[\</mo\>\<mi\>n\</mi\>\<mo\>\]\</mo\>\<mo\>)\</mo\>\<mo\>-\</mo\>\<mo\>sgn\</mo\>\<mo\>(\</mo\>\<mi\>x\</mi\>\<mo\>\[\</mo\>\<mi\>n\</mi\>\<mo\>-\</mo\>\<mn\>1\</mn\>\<mo\>\]\</mo\>\<mo\>)\</mo\>\</mrow\>\</mfenced\>\</mstyle\>\</math\>","truncated":false}][image1]

Trong đó: x\[n\] là mẫu tín hiệu tại thời điểm n, N là số mẫu trong khung, sign(.) là hàm lấy dấu của tín hiệu.

**Lý do lựa chọn:** ZCR được chọn vì nó phản ánh mức dao động nhanh của tín hiệu. Âm thanh sắc, nhiều âm cao, tiếng gõ hoặc nhiễu thường có ZCR cao; âm thanh trầm, mềm thường có ZCR thấp.

**Giá trị thông tin:** ZCR giúp phân biệt các đoạn nhạc có tính chất dao động khác nhau, hỗ trợ nhận biết bản nhạc có tiết tấu mạnh hoặc nhiều thành phần cao tần.

**Ví dụ:** Một đoạn nhạc có nhiều tiếng guitar gảy nhanh, tiếng hi-hat hoặc tiếng gõ sắc thường có ZCR cao vì tín hiệu dao động và đổi dấu liên tục. Ngược lại, một đoạn nhạc piano nhẹ, kéo dài hoặc âm bass trầm thường có ZCR thấp vì tín hiệu thay đổi chậm và ít dao động nhanh. 

### ***2.2.2. RMS Energy***

**Khái niệm:** RMS Energy biểu diễn năng lượng hiệu dụng trung bình của tín hiệu trong một khung thời gian.

**Công thức:** 

![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>R\</mi\>\<mi\>M\</mi\>\<mi\>S\</mi\>\<mo\>=\</mo\>\<msqrt\>\<mfrac\>\<mn\>1\</mn\>\<mi\>N\</mi\>\</mfrac\>\<munderover\>\<mo\>&\#x2211;\</mo\>\<mrow\>\<mi\>n\</mi\>\<mo\>=\</mo\>\<mn\>0\</mn\>\</mrow\>\<mrow\>\<mi\>N\</mi\>\<mo\>-\</mo\>\<mn\>1\</mn\>\</mrow\>\</munderover\>\<msup\>\<mi\>x\</mi\>\<mn\>2\</mn\>\</msup\>\<mo\>\[\</mo\>\<mi\>n\</mi\>\<mo\>\]\</mo\>\</msqrt\>\</mstyle\>\</math\>","truncated":false}][image2]

Trong đó: x\[n\] là giá trị biên độ của mẫu âm thanh, N là số mẫu trong khung.

**Lý do lựa chọn:** RMS được chọn vì nó phản ánh độ mạnh/yếu của âm thanh. Những đoạn nhạc mạnh, nhiều nhạc cụ hoặc có cao trào thường có RMS cao.

Giá trị thông tin: RMS giúp so sánh mức năng lượng tổng thể giữa các đoạn nhạc, phân biệt nhạc nhẹ, nhạc mạnh, đoạn cao trào và đoạn trầm lắng.

Ví dụ: Một đoạn cao trào có nhiều nhạc cụ cùng chơi, âm lượng lớn và tiết tấu mạnh thường có RMS cao. Ngược lại, đoạn mở đầu chỉ có tiếng piano nhẹ hoặc âm thanh nền nhỏ thường có RMS thấp. 

### ***2.2.3. Tempo***

**Khái niệm:** Tempo là nhịp độ của bản nhạc, thường được đo bằng BPM, tức số nhịp trong một phút.

**Công thức:**

**![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>B\</mi\>\<mi\>P\</mi\>\<mi\>M\</mi\>\<mo\>=\</mo\>\<mfrac\>\<mrow\>\<mi\>n\</mi\>\<mo\>&\#xD7;\</mo\>\<mn\>60\</mn\>\</mrow\>\<mi\>t\</mi\>\</mfrac\>\</mstyle\>\</math\>","truncated":false}][image3]** 

Trong đó: n là số nhịp, t là thời gian tính bằng s

**Lý do lựa chọn:** Tempo được chọn vì nhịp độ là yếu tố quan trọng trong cảm nhận âm nhạc. Các bản nhạc có phong cách tương tự thường có tốc độ gần nhau.

**Giá trị thông tin:** Tempo giúp phân biệt nhạc chậm, nhạc nhanh, nhạc thư giãn và nhạc sôi động; đồng thời hỗ trợ tìm các bản nhạc có tiết tấu tương đồng.

**Ví dụ:** Một bản nhạc dance hoặc nhạc sôi động có thể có tempo khoảng 120–140 BPM, tạo cảm giác nhanh và mạnh. Trong khi đó, một bản nhạc thư giãn hoặc piano ballad có thể có tempo khoảng 60–80 BPM, tạo cảm giác chậm và nhẹ nhàng.

### ***2.2.4. Onset Strength***

**Khái niệm:** Onset Strength đo mức độ thay đổi năng lượng phổ tại thời điểm xuất hiện sự kiện âm thanh mới như nốt nhạc hoặc tiếng gõ.

**Công thức:**

![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>O\</mi\>\<mi\>n\</mi\>\<mi\>s\</mi\>\<mi\>e\</mi\>\<mi\>t\</mi\>\<mo\>(\</mo\>\<mi\>t\</mi\>\<mo\>)\</mo\>\<mo\>=\</mo\>\<munder\>\<mo\>&\#x2211;\</mo\>\<mi\>k\</mi\>\</munder\>\<mi\>max\</mi\>\<mo\>(\</mo\>\<mn\>0\</mn\>\<mo\>,\</mo\>\<mi\>S\</mi\>\<mo\>(\</mo\>\<mi\>k\</mi\>\<mo\>,\</mo\>\<mi\>t\</mi\>\<mo\>)\</mo\>\<mo\>-\</mo\>\<mi\>S\</mi\>\<mo\>(\</mo\>\<mi\>k\</mi\>\<mo\>,\</mo\>\<mi\>t\</mi\>\<mo\>-\</mo\>\<mn\>1\</mn\>\<mo\>)\</mo\>\<mo\>)\</mo\>\</mstyle\>\</math\>","truncated":false}][image4]

Trong đó: S\[f,t\] là biên độ phổ tại dải tần số f và thời điểm t.

**Lý do lựa chọn:** Onset Strength được chọn vì nó phản ánh độ rõ của nhịp, tiếng gõ và các điểm bắt đầu âm trong bản nhạc.

**Giá trị thông tin:** Đặc trưng này giúp phân biệt nhạc có tiết tấu rõ, nhiều nhạc cụ gõ với nhạc mềm, liền mạch hoặc ít nhịp rõ.

**Ví dụ:** Một đoạn nhạc có tiếng trống, tiếng guitar gảy rõ từng nhịp hoặc các nốt piano được đánh tách bạch thường có Onset Strength cao. Ngược lại, một đoạn nhạc nền kéo dài, âm thanh liền mạch như violin legato hoặc pad synth thường có Onset Strength thấp. 

## **2.3. Thuộc tính trên miền tần số**

Miền tần số biểu diễn tín hiệu âm thanh theo các thành phần tần số sau khi biến đổi Fourier hoặc biến đổi phổ ngắn hạn. Các thuộc tính miền tần số giúp mô tả âm sắc, cao độ, hòa âm, độ sáng âm thanh và phân bố năng lượng phổ.

### ***2.3.1. Spectral Centroid***

**Khái niệm:** Spectral Centroid là trọng tâm của phổ tần số, cho biết năng lượng phổ tập trung nhiều ở vùng tần số thấp hay cao.

**Công thức:**

**![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>C\</mi\>\<mi\>e\</mi\>\<mi\>n\</mi\>\<mi\>t\</mi\>\<mi\>r\</mi\>\<mi\>o\</mi\>\<mi\>i\</mi\>\<mi\>d\</mi\>\<mo\>=\</mo\>\<mfrac\>\<mrow\>\<msub\>\<mo\>&\#x2211;\</mo\>\<mi\>k\</mi\>\</msub\>\<mi\>f\</mi\>\<mo\>\[\</mo\>\<mi\>k\</mi\>\<mo\>\]\</mo\>\<mo\>&\#xB7;\</mo\>\<mo\>|\</mo\>\<mi\>X\</mi\>\<mo\>\[\</mo\>\<mi\>k\</mi\>\<mo\>\]\</mo\>\<mo\>|\</mo\>\</mrow\>\<mrow\>\<msub\>\<mo\>&\#x2211;\</mo\>\<mi\>k\</mi\>\</msub\>\<mo\>|\</mo\>\<mi\>X\</mi\>\<mo\>\[\</mo\>\<mi\>k\</mi\>\<mo\>\]\</mo\>\<mo\>|\</mo\>\</mrow\>\</mfrac\>\</mstyle\>\</math\>","truncated":false}][image5]**

Trong đó: f\[k\] là tần số tại bin k, |X\[k\]| là biên độ phổ tại bin k.

**Lý do lựa chọn:** Spectral Centroid được chọn vì nó phản ánh độ sáng hoặc độ trầm của âm thanh.

**Giá trị thông tin:** Giá trị cao cho thấy âm thanh sáng, sắc, nhiều âm cao; giá trị thấp cho thấy âm thanh trầm, ấm.

**Ví dụ:** Một đoạn nhạc có nhiều tiếng cymbal, violin cao hoặc âm thanh sáng thường có Spectral Centroid cao vì năng lượng tập trung nhiều ở vùng tần số cao. Ngược lại, đoạn nhạc có tiếng bass, cello hoặc âm trầm sẽ có Spectral Centroid thấp vì năng lượng tập trung ở vùng tần số thấp. 

### ***2.3.2. Spectral Bandwidth***

**Khái niệm:** Spectral Bandwidth đo độ phân tán của phổ tần số quanh Spectral Centroid.

**Công thức:**

![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>B\</mi\>\<mi\>a\</mi\>\<mi\>n\</mi\>\<mi\>d\</mi\>\<mi\>w\</mi\>\<mi\>i\</mi\>\<mi\>d\</mi\>\<mi\>t\</mi\>\<mi\>h\</mi\>\<mo\>=\</mo\>\<msup\>\<mfenced\>\<mfrac\>\<mrow\>\<msub\>\<mo\>&\#x2211;\</mo\>\<mi\>k\</mi\>\</msub\>\<mo\>|\</mo\>\<mi\>X\</mi\>\<mo\>\[\</mo\>\<mi\>k\</mi\>\<mo\>\]\</mo\>\<mo\>|\</mo\>\<mo\>&\#xB7;\</mo\>\<mo\>(\</mo\>\<mi\>f\</mi\>\<mo\>\[\</mo\>\<mi\>k\</mi\>\<mo\>\]\</mo\>\<mo\>-\</mo\>\<mi\>C\</mi\>\<mi\>e\</mi\>\<mi\>n\</mi\>\<mi\>t\</mi\>\<mi\>r\</mi\>\<mi\>o\</mi\>\<mi\>i\</mi\>\<mi\>d\</mi\>\<msup\>\<mo\>)\</mo\>\<mi\>p\</mi\>\</msup\>\</mrow\>\<mrow\>\<msub\>\<mo\>&\#x2211;\</mo\>\<mi\>k\</mi\>\</msub\>\<mo\>|\</mo\>\<mi\>X\</mi\>\<mo\>\[\</mo\>\<mi\>k\</mi\>\<mo\>\]\</mo\>\<mo\>|\</mo\>\</mrow\>\</mfrac\>\</mfenced\>\<mfrac\>\<mn\>1\</mn\>\<mi\>p\</mi\>\</mfrac\>\</msup\>\</mstyle\>\</math\>","truncated":false}][image6]

Trong đó: f\[k\] là tần số bin k, |X\[k\]| là biên độ phổ của tần số thứ k , p là bậc của phép đo khoảng cách phổ, thông thường p=2. 

**Lý do lựa chọn:** Spectral Bandwidth được chọn vì nó thể hiện phổ âm thanh rộng hay hẹp, đơn giản hay phong phú.

**Giá trị thông tin:** Đặc trưng này giúp phân biệt bản nhạc có phối khí dày, nhiều thành phần tần số với bản nhạc đơn giản, phổ hẹp.

**Ví dụ:** Một đoạn nhạc có nhiều nhạc cụ cùng xuất hiện như piano, violin, trống, bass thường có Spectral Bandwidth cao vì phổ tần số trải rộng trên nhiều vùng. Ngược lại, một đoạn chỉ có một nhạc cụ đơn giản như sáo hoặc piano đơn âm thường có Spectral Bandwidth thấp hơn vì phổ tập trung trong phạm vi hẹp. 

### ***2.3.3. MFCC***

**Khái niệm:** MFCC là các hệ số cepstral trên thang Mel, mô phỏng cách tai người cảm nhận tần số âm thanh.

**Công thức:**

**![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>M\</mi\>\<mi\>F\</mi\>\<mi\>C\</mi\>\<msub\>\<mi\>C\</mi\>\<mi\>i\</mi\>\</msub\>\<mo\>=\</mo\>\<mi\>D\</mi\>\<mi\>C\</mi\>\<mi\>T\</mi\>\<mo\>(\</mo\>\<mi\>log\</mi\>\<mo\>(\</mo\>\<msub\>\<mi\>E\</mi\>\<mrow\>\<mi\>m\</mi\>\<mi\>e\</mi\>\<mi\>l\</mi\>\</mrow\>\</msub\>\<mo\>)\</mo\>\<msub\>\<mo\>)\</mo\>\<mi\>i\</mi\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image7]**

Trong đó: ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<msub\>\<mi\>E\</mi\>\<mrow\>\<mi\>m\</mi\>\<mi\>e\</mi\>\<mi\>l\</mi\>\</mrow\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image8] là năng lượng sau khi tín hiệu đi qua các bộ lọc Mel; DCT là biến đổi Cosine rời rạc.

**Lý do lựa chọn:** MFCC được chọn vì đây là đặc trưng rất phổ biến trong nhận dạng âm thanh, có khả năng mô tả âm sắc và cấu trúc phổ.

**Giá trị thông tin:** MFCC giúp phân biệt chất âm, nhạc cụ, cách phối âm và màu sắc âm thanh giữa các bản nhạc.

**Ví dụ:** Cùng một giai điệu nhưng được chơi bằng piano và guitar sẽ tạo ra các giá trị MFCC khác nhau vì hai nhạc cụ có âm sắc và cấu trúc phổ khác nhau. Nhờ đó, MFCC giúp hệ thống phân biệt chất âm, nhạc cụ và cách phối âm của bản nhạc. 

### ***2.3.4. Chroma Feature***

**Khái niệm:** Chroma biểu diễn năng lượng âm thanh theo 12 lớp cao độ tương ứng 12 nốt nhạc trong một quãng tám.

**Công thức:**

**![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>C\</mi\>\<mi\>h\</mi\>\<mi\>r\</mi\>\<mi\>o\</mi\>\<mi\>m\</mi\>\<mi\>a\</mi\>\<mo\>\[\</mo\>\<mi\>c\</mi\>\<mo\>\]\</mo\>\<mo\>=\</mo\>\<munder\>\<mo\>&\#x2211;\</mo\>\<mrow\>\<mi\>k\</mi\>\<mo\>&\#x2208;\</mo\>\<mi\>c\</mi\>\</mrow\>\</munder\>\<mo\>|\</mo\>\<mi\>X\</mi\>\<mo\>\[\</mo\>\<mi\>k\</mi\>\<mo\>\]\</mo\>\<msup\>\<mo\>|\</mo\>\<mn\>2\</mn\>\</msup\>\</mstyle\>\</math\>","truncated":false}][image9]**

**Giải thích công thức:** Trong đó c là một trong 12 lớp cao độ: C, C\#, D, D\#, E, F, F\#, G, G\#, A, A\#, B.

**Lý do lựa chọn:** Chroma được chọn vì nó phản ánh giai điệu, hợp âm và cấu trúc cao độ, rất phù hợp với nhạc không lời.

**Giá trị thông tin:** Đặc trưng này giúp phát hiện các bản nhạc có giai điệu hoặc hòa âm tương đồng dù cách phối khí khác nhau.

**Ví dụ:** Hai đoạn nhạc có cùng vòng hợp âm hoặc cùng giai điệu chính, dù được chơi bằng nhạc cụ khác nhau như piano hoặc guitar, vẫn có Chroma Feature khá giống nhau. Ngược lại, hai đoạn có giai điệu hoặc hợp âm khác nhau sẽ có phân bố Chroma khác nhau. 

### ***2.3.5. Spectral Contrast***

**Khái niệm:** Spectral Contrast đo sự khác biệt giữa các đỉnh phổ và đáy phổ trong từng dải tần số.

**Công thức:**

**![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>C\</mi\>\<mi\>o\</mi\>\<mi\>n\</mi\>\<mi\>t\</mi\>\<mi\>r\</mi\>\<mi\>a\</mi\>\<mi\>s\</mi\>\<msub\>\<mi\>t\</mi\>\<mi\>b\</mi\>\</msub\>\<mo\>=\</mo\>\<mi\>m\</mi\>\<mi\>e\</mi\>\<mi\>a\</mi\>\<mi\>n\</mi\>\<mo\>(\</mo\>\<mi\>P\</mi\>\<mi\>e\</mi\>\<mi\>a\</mi\>\<msub\>\<mi\>k\</mi\>\<mi\>b\</mi\>\</msub\>\<mo\>)\</mo\>\<mo\>-\</mo\>\<mi\>m\</mi\>\<mi\>e\</mi\>\<mi\>a\</mi\>\<mi\>n\</mi\>\<mo\>(\</mo\>\<mi\>V\</mi\>\<mi\>a\</mi\>\<mi\>l\</mi\>\<mi\>l\</mi\>\<mi\>e\</mi\>\<msub\>\<mi\>y\</mi\>\<mi\>b\</mi\>\</msub\>\<mo\>)\</mo\>\</mstyle\>\</math\>","truncated":false}][image10]**

Trong đó: ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>P\</mi\>\<mi\>e\</mi\>\<mi\>a\</mi\>\<msub\>\<mi\>k\</mi\>\<mi\>b\</mi\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image11] là nhóm giá trị phổ lớn nhất và ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>V\</mi\>\<mi\>a\</mi\>\<mi\>l\</mi\>\<mi\>l\</mi\>\<mi\>e\</mi\>\<msub\>\<mi\>y\</mi\>\<mi\>b\</mi\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image12] là nhóm giá trị phổ nhỏ nhất trong dải tần b.

**Lý do lựa chọn:** Spectral Contrast được chọn vì nó thể hiện mức độ tương phản và độ phức tạp của phổ âm thanh.

**Giá trị thông tin:** Giúp phân biệt nhạc có nhiều lớp âm thanh, phối khí phức tạp với nhạc đơn giản hoặc ít nhạc cụ.

**Ví dụ:** Một đoạn nhạc có nhiều lớp âm thanh, ví dụ vừa có giai điệu piano nổi bật, vừa có nền dây và tiếng trống, thường có Spectral Contrast cao vì có sự chênh lệch rõ giữa các đỉnh phổ và đáy phổ. Ngược lại, một đoạn nhạc nền đều, ít nhạc cụ hoặc âm thanh trải phẳng thường có Spectral Contrast thấp hơn. 

## **2.4. Bảng tổng hợp bộ thuộc tính đề xuất**

| Nhóm | Thuộc tính | Ý nghĩa | Vai trò |
| ----- | ----- | ----- | ----- |
| Miền thời gian  | ZCR | Mức đổi dấu của tín hiệu | Phân biệt tín hiệu dao động nhanh/chậm |
|  | RMS | Năng lượng hiệu dụng | So sánh độ mạnh/yếu âm thanh |
|  | Tempo | Nhịp độ BPM | Tìm bản nhạc có tốc độ tương tự |
|  | Onset Strength | Độ rõ điểm bắt đầu âm | So sánh cấu trúc tiết tấu |
| Miền tần số | Spectral Centroid | Trọng tâm phổ | Phân biệt âm sáng/trầm |
|  | Spectral Bandwidth | Độ rộng phổ | Đánh giá độ phong phú phổ |
|  | MFCC | Âm sắc trên thang Mel | Nhận diện chất âm và nhạc cụ |
|  | Chroma | Cao độ và hợp âm | Nhận diện giai điệu, hòa âm |
|  | Spectral Contrast | Tương phản phổ | Phân biệt độ phức tạp phối khí |

## **2.5. Vector đặc trưng đề xuất**

Mỗi file âm thanh được chia thành nhiều đoạn ngắn bằng cơ chế cửa sổ trượt. Với mỗi đoạn âm thanh, hệ thống trích xuất một vector đặc trưng gồm các thuộc tính trên miền thời gian và miền tần số. 

**Feature Vector \=**

\[

    ZCR,

    RMS,

    Tempo,

    Onset Strength,

    Spectral Centroid,

    Spectral Bandwidth,

    MFCC\_1, MFCC\_2, ..., MFCC\_13,

    Chroma\_1, Chroma\_2, ..., Chroma\_12,

    SpectralContrast\_1, SpectralContrast\_2, ..., SpectralContrast\_7

\]

**Trong đó:** ZCR, RMS, Tempo, Onset, Spectral Centroid, Spectral Bandwidth và mỗi loại 1 giá trị; MFCC gồm 13 hệ số; Chroma gồm 12 hệ số; Spectral Contrast gồm 7 hệ số, thì mỗi đoạn âm thanh được biểu diễn bằng vector 38 chiều.

# **PHẦN 3\. XÂY DỰNG CSDL VÀ CƠ CHẾ TÌM KIẾM NHẠC TƯƠNG ĐỒNG**

## **3.1. Mô hình dữ liệu tổng quát**

Hệ cơ sở dữ liệu được thiết kế gồm hai nhóm dữ liệu chính:

1. Dữ liệu quản lý file âm thanh.

2. Dữ liệu quản lý vector đặc trưng của từng đoạn âm thanh.

**Trong đó:**

- Mỗi file âm thanh được lưu trong bảng tracks.

- Mỗi file âm thanh có thể được chia thành nhiều đoạn nhỏ.

- Mỗi đoạn nhỏ có một vector đặc trưng riêng, được lưu trong bảng track\_segments.

**Quan hệ giữa hai bảng:** là quan hệ một \- nhiều. 1 file nhạc → nhiều đoạn âm thanh, 1 track → nhiều track\_segments

**Ví dụ:** File 0001\_Instrumental \- instrumental music.mp3 dài 30 giây

→ chia thành 11 đoạn.

→ lưu 11 vector đặc trưng trong bảng track\_segments.

### ***3.1.1. Thiết kế bảng tracks***

Bảng tracks dùng để lưu thông tin tổng quát của mỗi file âm thanh trong bộ dữ liệu. 

**Cấu trúc bảng:** 

| Tên trường | Kiểu dữ liệu | Ý nghĩa |
| ----- | ----- | ----- |
| track\_id  | INT | Mã định danh duy nhất của bản nhạc  |
| file\_name  | VARCHAR(100) | Tên file âm thanh  |
| file\_path  | VARCHAR(100) | Đường dẫn lưu file âm thanh  |
| duration  | FLOAT  | Thời lượng file âm thanh, tính bằng giây  |
| format  | VARCHAR(5) | Định dạng file |

### ***3.1.2. Thiết kế bảng track\_segments***

Bảng track\_segments dùng để lưu thông tin từng đoạn âm thanh sau khi file được chia bằng cửa sổ trượt. Mỗi đoạn có thời gian bắt đầu, thời gian kết thúc và vector đặc trưng tương ứng. Với file dài 30 giây, nếu dùng cửa sổ 5 giây và bước trượt 2,5 giây, mỗi file sẽ tạo khoảng 11 đoạn. Vì vậy, bộ dữ liệu có 1000 file, tổng số vector đoạn khoảng: 1000 × 11 \= 11000 vector.

**Cấu trúc bảng:** 

| Tên trường | Kiểu dữ liệu | Ý nghĩa |
| ----- | ----- | ----- |
| segment\_id | INT | Mã định danh của đoạn âm thanh |
| track\_id | INT | Mã file nhạc tương ứng |
| segment\_index | INT | Thứ tự đoạn trong file |
| start\_time | FLOAT | Thời điểm bắt đầu đoạn, tính bằng giây |
| end\_time | FLOAT | Thời điểm kết thúc đoạn, tính bằng giây |
| zcr | FLOAT | Giá trị Zero Crossing Rate |
| rms | FLOAT | Giá trị RMS Energy |
| tempo | FLOAT | Giá trị nhịp độ BPM |
| onset\_strength | FLOAT | Cường độ điểm bắt đầu âm |
| spectral\_centroid | FLOAT | Trọng tâm phổ |
| spectral\_bandwidth | FLOAT | Độ rộng phổ |
| mfcc | JSON  | Mảng 13 hệ số MFCC |
| chroma | JSON  | Mảng 12 hệ số Chroma |
| spectral\_contrast | JSON | Mảng hệ số Spectral Contrast |
| feature\_vector | JSON | Vector đặc trưng tổng hợp gốc |
| normalized\_vector  | JSON | Vector đặc trưng tổng hợp đã chuẩn hóa |

	

## **3.2. Cơ chế trích xuất và lưu trữ metadata**

Quy trình trích xuất và lưu trữ siêu dữ liệu được thực hiện như sau:

1. Đọc file âm thanh.

2. Chia file thành các đoạn nhỏ bằng cửa sổ trượt.

3. Trích xuất đặc trưng cho từng đoạn.

4. Ghép các đặc trưng thành vector tổng hợp.

5. Chuẩn hóa vector đặc trưng về \[0,1\].

6. Lưu thông tin file vào bảng tracks.

7. Lưu vector đặc trưng gốc và vector đã chuẩn hóa của từng đoạn vào bảng track\_segments.

Đầu tiên, hệ thống đọc file âm thanh và chuyển tín hiệu âm thanh thành chuỗi mẫu số. Sau đó, file được chia thành nhiều đoạn ngắn bằng cửa sổ trượt. Với file âm thanh dài khoảng 30 giây, hệ thống sử dụng cửa sổ 5 giây và bước trượt 2,5 giây. Như vậy, mỗi file tạo ra khoảng 11 đoạn âm thanh.

Với mỗi đoạn, hệ thống trích xuất các đặc trưng trên miền thời gian và miền tần số như ZCR, RMS, Tempo, Onset Strength, Spectral Centroid, Spectral Bandwidth, MFCC, Chroma và Spectral Contrast. Các đặc trưng này được ghép lại thành một vector đặc trưng tổng hợp gồm 38 chiều.

Sau khi tạo vector đặc trưng, hệ thống chuẩn hóa vector về khoảng \[0,1\] bằng phương pháp Min-Max Normalization:

![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>x\</mi\>\<mo\>'\</mo\>\<mo\>=\</mo\>\<mfrac\>\<mrow\>\<mi\>x\</mi\>\<mo\>-\</mo\>\<msub\>\<mi\>x\</mi\>\<mi\>min\</mi\>\</msub\>\</mrow\>\<mrow\>\<msub\>\<mi\>x\</mi\>\<mi\>max\</mi\>\</msub\>\<mo\>-\</mo\>\<msub\>\<mi\>x\</mi\>\<mi\>min\</mi\>\</msub\>\</mrow\>\</mfrac\>\</mstyle\>\</math\>","truncated":false}][image13]

Trong đó: x là giá trị đặc trưng ban đầu, ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<msub\>\<mi\>x\</mi\>\<mrow\>\<mi\>m\</mi\>\<mi\>i\</mi\>\<mi\>n\</mi\>\</mrow\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image14] và ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<msub\>\<mi\>x\</mi\>\<mrow\>\<mi\>m\</mi\>\<mi\>a\</mi\>\<mi\>x\</mi\>\</mrow\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image15] lần lượt là giá trị nhỏ nhất và lớn nhất của thuộc tính đó trong toàn bộ cơ sở dữ liệu. 

Việc chuẩn hóa giúp các thuộc tính có thang đo khác nhau được đưa về cùng một miền giá trị, tránh trường hợp các đặc trưng có giá trị lớn như Spectral Centroid hoặc Spectral Bandwidth chi phối kết quả tìm kiếm.

Đối với quá trình xây dựng cơ sở dữ liệu ban đầu, hệ thống cần trích xuất toàn bộ vector gốc trước để tính ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<msub\>\<mi\>x\</mi\>\<mrow\>\<mi\>m\</mi\>\<mi\>i\</mi\>\<mi\>n\</mi\>\</mrow\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image14] và ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<msub\>\<mi\>x\</mi\>\<mrow\>\<mi\>m\</mi\>\<mi\>a\</mi\>\<mi\>x\</mi\>\</mrow\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image15] cho từng chiều đặc trưng. Sau đó, các vector gốc được chuẩn hóa và lưu vào cơ sở dữ liệu. Khi có file truy vấn mới, vector đặc trưng của file truy vấn cũng được chuẩn hóa bằng cùng các tham số ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<msub\>\<mi\>x\</mi\>\<mrow\>\<mi\>m\</mi\>\<mi\>i\</mi\>\<mi\>n\</mi\>\</mrow\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image14] và ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<msub\>\<mi\>x\</mi\>\<mrow\>\<mi\>m\</mi\>\<mi\>a\</mi\>\<mi\>x\</mi\>\</mrow\>\</msub\>\</mstyle\>\</math\>","truncated":false}][image15] này.

Cuối cùng, thông tin chung của file âm thanh được lưu vào bảng tracks, còn vector đặc trưng của từng đoạn được lưu vào bảng track\_segments.

## **3.3. Cơ chế tìm kiếm bản nhạc tương đồng**

Khi người dùng đưa vào một file âm thanh truy vấn, hệ thống thực hiện các bước:

1. Nhận file âm thanh truy vấn

2. Đọc và tiền xử lý file truy vấn

3. Chia file truy vấn thành các đoạn nhỏ bằng cửa sổ trượt

4. Trích xuất vector đặc trưng cho từng đoạn

5. Chuẩn hóa vector đặc trưng của truy vấn về \[0,1\]

6. Lấy các vector đặc trưng đã chuẩn hóa trong cơ sở dữ liệu

7. Tính độ tương đồng giữa vector truy vấn và vector trong cơ sở dữ liệu

8. Tổng hợp điểm tương đồng theo từng file nhạc

9. Sắp xếp các file theo điểm tương đồng giảm dần

10. Trả về 5 file âm thanh giống nhất

## **3.4. Phương pháp tính độ tương đồng** 

Để so sánh hai vector đặc trưng, hệ thống có thể sử dụng Cosine Similarity.

Với vector truy vấn là A, vector trong cơ sở dữ liệu là B. Độ tương đồng cosine được tính:

![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>cos\</mi\>\<mo\>(\</mo\>\<mi\>A\</mi\>\<mo\>,\</mo\>\<mi\>B\</mi\>\<mo\>)\</mo\>\<mo\>=\</mo\>\<mfrac\>\<mrow\>\<mi\>A\</mi\>\<mo\>&\#xB7;\</mo\>\<mi\>B\</mi\>\</mrow\>\<mrow\>\<mo\>&\#x2016;\</mo\>\<mi\>A\</mi\>\<mo\>&\#x2016;\</mo\>\<mo\>&\#x2016;\</mo\>\<mi\>B\</mi\>\<mo\>&\#x2016;\</mo\>\</mrow\>\</mfrac\>\</mstyle\>\</math\>","truncated":false}][image16]

Trong đó: ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mi\>A\</mi\>\<mo\>&\#xB7;\</mo\>\<mi\>B\</mi\>\</mstyle\>\</math\>","truncated":false}][image17] là tích vô hướng của 2 vector. ![{"mathml":"\<math style=\\"font-family:stix;font-size:16px;\\" xmlns=\\"http://www.w3.org/1998/Math/MathML\\"\>\<mstyle mathsize=\\"16px\\"\>\<mo\>&\#x2016;\</mo\>\<mi\>A\</mi\>\<mo\>&\#x2016;\</mo\>\<mo\>,\</mo\>\<mo\>&\#xA0;\</mo\>\<mo\>&\#x2016;\</mo\>\<mi\>B\</mi\>\<mo\>&\#x2016;\</mo\>\</mstyle\>\</math\>","truncated":false}][image18] là độ dài của vector A, B.

Giá trị cosine similarity nằm trong khoảng \[0,1\] do đó:

- cos(A,B) càng gần 1 thì 2 đoạn âm thanh rất giống nhau.  
- cos(A,B) càng gần 0 thì 2 đoạn âm thanh rất khác nhau.

# **PHẦN 4\. XÂY DỰNG HỆ THỐNG**

## **4.1. Sơ đồ khối của hệ thống**

## **4.2. Quy trình thực hiện yêu cầu**

## **4.3. Kết quả tìm kiếm đạt được**

4.3.1. File âm thanh có sẵn

4.3.2. File âm thanh không có sẵn

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJMAAAA5CAYAAAAyYhmdAAAEd0lEQVR4Xu2cPatTQRCGFxERsdBKLUQLCysR/BNWIlb+AisRC0FBQSysBCvRQiSIiCCWdhaWNnY2IliIiIggoqAggmZyzt5M3sycj9k9m3Nv5oElZ979mN2duTk3ySYhrB//vAxW1g5a9ARFx7Gwln9BzjB4MjlZOD0tP1F0HAv0rLQfRcexUOIWJ72yyfGK5wwKzmpJCWYfpMRBuy+p/Z3MlArIwZDfV+7xnERKBuRDmPv7yyuMlJy704ESAXnJrqO/HH5zjOFkpERAuI+c/nKO5WTgHgoDsA3sXEmQaxwnA1dQ6EHXQErtJM1CrnGcDFiDQf2sfZ0tijUhPJmcJawJ4cnkLGFNCEsyHQ3zfinFGSnW4FgDS6cTMDn6FmekWIOTElhrcvRt7xRkZ7AHJzWwKQnljJDPwf4+U98kQK4FT6YtRUpg+iaBhOXZ6REKRp6Gfn6dFqwbaUkCjZxjdWU3u0651TuMsWxi6YR6BnYJnxvsCosOtUVrekSqJ/tSfX2htktR0lcTe8JiMr1ZrB6cP+xailEfWvteDcuNJKeSFol1T5h2oNY4aA9JSV9t8GQqOS/0leq/ta/kQNLo6RM1ImpY90vQ0B6Skr66EPdU2tsh+IRCSPfd2hcb0CRQO1E/kn6MV0w5Py1v6zqENKorzdlQvTUwNnIkU/wjpTsK8aW2m4j1ku/rtXa5tqU2EU3fgC9QG4hP5qOia/2oPMAKBvqWSl+oD31WNjas60HuhGqck1hRo+0f2pGofQcb0fQZfHDNESG1wUmeYzbnR6jqd2DFgGjriMR1pJS+WPtpWMbS5oC61IbQ9BldB4k8D/M2k/pxL9M00M/QlPTVhbj+7ViRgGWNUhxuhOpbNRxsE9H0GVhJ9mtBQ5traGtobWL/piKh6URTXWluhWo+x7EigXfBtkZpPyVbu8tg2w3i7YdzX9C62JKGSFoKTeM11ZVG2p8c3AzVP+ME/ThHF6S5aPbXBbUC287gB7nwH1XuUHuVFoltsQ3X6JsbWJ9KHP83VtTk9mdF2ps2tPaPw3Id2fRqris4Hyk22Iaj6ZsWfEdZQtNL0jS/Jl6gkBHrnCIpfUfN4SAv7lWwf1dO22x6z0rSNbRx2rD06YN1XpGUvqNHWpykdUXb7LsoNHAkVGNcxIoWNN9OIaTNl7SuxLc5KCE4fcaMSWEtzoqgzZ8ImoV99aMUVLQ1MDEsxVkR9GoOA4B2V3g/yxiYFNbirBAMANpd4f14YK3jOZsQDDbaXcGPOjyZ1hAKNp115nZfpD6k0QkJ/LmcoTkVqtOp0pycgeG3JEoq7VhGE1rgNH1IuM9V+F9reDJZzlcfCnrQNH0o+FkxorR/J8w3fZWbTx+D8HlY5oJ9HobqJKRTkDEkE0H+6cxXvO4L9rkdFr+k4RSAgjCpH1cFnYXnR0Liufk+4Py/ge0UIN5WMBgl4b6lefA5YuHwg2lY5xSAfqBCCkxJMJmsc+H9cvwwvWMgJYCOswAl0nsUHceCPzM52fBEchzHcab8B3mbkMH03vYpAAAAAElFTkSuQmCC>

[image3]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGEAAAAhCAYAAADJXsXPAAAB7klEQVR4Xu2YMUoEQRBFKxADEcHAQAwEMRBTYzMDAwOv4AW8gBh6Cg9gIsZewUSMRAQxMjAxEgMTnWK7sPbP75kB3Zm1tx40O/9XdWtX7c70rkjwV3xVYwG8peTrCCaIFngNzYqParw7HY2YEE2Fxdgm8YKKZckXpu020hTPxZhXLL4Ir6AZGGvLVzS+kV4xH7XBvKLBDaP2rMhPPFdAz77Uc/y83BrMKxbd7J3TD8lrQ3Oe0SScC18vmuDQzX6CvnGaYYXrWiiWF01w4GZRIxrXT4vXbbAc72F8kXhFg5tF7dHYPZrSPEfRB/6T08dSb8IR6JmBbZZ5yraMPzuQ3DxjXUY5ubwtaY4H0wp2DbWBvl4/Om2wuQauESRYYVArXfJOkncJvmLzcU4go6L4o515SBevrdDqX6EZ1AvGinhBvGviaTP1V0T0TaMfVJzJ+Ls3VyQfOwRt7KTXVRmP+QbgHAP/BzaKhW1Q9Tzx9sBD/Dp2/QYe/q3fgE36L6MGM1kyaobPsesX4gUOvG0Y2ATUXcA5B6ARy28aRcI2l/Pw9ITg9wW2BnozD77LckXysdzRUhuE80/dtV/j1vlBEARBJ3bRCPqFPR+DHmk6qAQ9obehaMDAaAP0B8tgQOJTMAVEEwZmTqIJg9PbqegbJIAWy9uNZPsAAAAASUVORK5CYII=>

[image4]: <data:image/png;base64,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>

[image5]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALwAAABACAYAAACgGR3JAAAFgElEQVR4Xu2dMaj0RBSFBxFLUUQsRJ6FhYiFICJWIlhZiIWFjYWNpdhZiYiIjYiI2FiKnaCI2IiIWFjYiIXY/YiIiJ2Figq/e/6XcW/Ou3cmmST7kt3zwZDMuTczs5mTfXm7STYlMYWrMxUhNgObt6UIsSmseX+iWAkZXmwWa/o7+6GQJ5IMLzZK62nKmFwhVkWL6YfmCbFKWkwvxGa5kvqGv74fXhUfsTADj6VlDvQ7duVtFgOWGoMIOOS7fG4/6ifSv01xDCA21GCWyGzQ/nA0m8t1S6RnbDwag1iQPHmlSZzKkHajHOgPsWhAfG7Ds+7VWctEesbGozGIBXkq9Q3/TT88C0MmNcqJ9Mzchn839XUvJzL8+8nXLTL8CrCGnxPbLspZP9wj6jvr+dSG81Cf0/Cgtj+imNVyjnd6lCmNQSzIXSmexKmgzd9YdPD6tmOKTmsQX8rwEVHcal4cyPArIJrAORjarpeXtZt7ap/I8F57lpLZfk7nsTMOdET7K2teLCPDXzLR5M3F0La9vDw2L5ZBbE7D/9ItS/16sbd25XtHZ2w8GoNYCG/i5uSGNLx9zrvXaByzRIavEZntHrPuxYG33+xYOWaR4S+JfEEYlktRm3wL56H+gVnHAQBu7ZaZOQ3v1T8mDXivy9Y5ZpHhLwlv0mr8yUKFMe1zrldnDUCbani8q0dtD9VtPcdvN1rG5snwB8KbsBrPszCAMX2MybW0Gn4KLfsv07qdaKR1smrbvMzCjq9ZKFBrP0KGFyH/pLYdPmSCc5yXQ/nLlCHY/DcptjS275bxigNwU9obt7WUqMWFOChs3pZSIseH5AqxKGzcllL6+PLBXXmYRSGOFRwQt7AoxLECw4NXe6oQR0o2fF6KBbHnmeA2E1sLOP/9l0Viq2bBdeqZ+9N2X8fqwY59kbQvO31t4AuY2rhqcXHClMxRio1lzrZqHLIvsSHs6YvHXJ8WoI/rWFwI9PU4i0LgK+SS2Rmba9f/NvVXunVul+sA2gO78mu3bnVLrY4bhX80dY6DR9N+XKUijpgxk8y5vP70rrxn6jaOhxJxP5+nizfkAs4DVsM/q7aO66t5G65PIb8WlW2WHq7ocHfa5+EUh7fhdrw43oVZ47wXHA1w2/aeTM73DgAhruGZzqOWx7FaHUQaP6KO++Z1bgd1HKCMTmlEdZJf75alvEfSxVit7p3igJr2BtV5XLiFzWsDyPDiGtFE43apDOdE6wDn5Tb/k279h/8zzuv4jJ/htry6bduu55sjeJu181Xqv67WIkaAG3lrOw+fpuBiez7l8OAbdTGpQ3k2nfeDO/Q9PqU6Dig8ki3zu1nfCmzeliLEpmgx8GtpXL4Qq8Ia/kOKlZDhxSbBLwGOfZcHY3KFWBUtpzZD84RYJS2mF2KzPJn6hr+vHxbi+DjEuzy3+12ncZ/2u5VnOi3X8bGwJfoNqefS/jsZG/dyxYmytOmjNj2dNa5n8JjrKAb4CcilXHGCLGn6qD3uy8vzNADdu5YpI8OLIp+lwxv+nbSPRTlj9YwML6osYXZQarPWZxSrmVmGF0XwDHmYIt9cMycls7UY3t434cWBDC9CYHIYAk8pXoLIbNa0ZzZg8LatmR3I8CIEZljSEFHbN3bLUv+eLsOLZkpmmwuvfatFN+oAT7eG9+JAhhcXKBkmYmw+4G24DqDhqRIM5/KYOZ6R4UWPL9K5CbAcQ4txpvx6Rq0//HV4icV00fBTxiCOAH6nHIL9dORQtPbHhhcnTIvZwZBtxv7FqJHHytfSRETX0ogTJRsBxhxS+ObvEniyhBCrwRq3tZSoxYU4GPkn66eWEjleyxNica7MVEpc7YoQRw+Mjl9xkeHFSZCNLsOLk8Aa/WRN/x/Ed5mZKDEhiwAAAABJRU5ErkJggg==>

[image6]: <data:image/png;base64,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>

[image7]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMAAAAARCAYAAACLvqONAAADaklEQVR4Xu2avYsUQRDFGzEUwUhETETEUBAxPAQxECMTMTASxNBAEKPDzNDAf8DIzEAMTMTAQMwMRMTUwEAQERERQfexU1zd29fV3Xc9c1/7g2a7XlVX9fQMuzPTm9KS7cohFgYezto/FjvykoW9Bhb3IosD8KnFj3TPGaFFY1lXWm+upMUar4XmUfOC/Wzo3yHdx/K4n2QreEwv3rKQQdW/x0JHVD3FZRZa+ZvmxX6wI62dODUZaPtZJHJjAetR7GMWOpOrHen4VmZuDZ/X1qmL6/vI9YHKxah5bJaWnC2xPTgxawdZFOD63RR2kvkAXwyf0E96xwDHMyqnx/tKsWMT1Wcd9nfSSnAOT+TzqLijs/Z71m6zY+B8mvsVKl+OaH3GpLZmbZzEblE4iX2bsQ44/oHrG/A/ZVFwKukardicSk2R04H3RTlyfEjxmMjn4bgWW82b7QjE/iF7Cmrr1MYt8Gr4xM8zL5h9quSm30jzi5xjzgotR65GK5an1Bj8uind8L5cjohoDJ4Xcj6mNA/WlD+yIyy3b1OAOp9ZFGx4PjbwgOvzIqr7Uy54l+yWRWqJHYOoPvvQr3lg9eRyA84fUZoHHgY5xuPtC2RHtMyxN7W1EYMv42aeuD6SnHa2aUzNpGpijJbYCMtTaozSDPj2kf3L2SVwDx7lf55iv8fHqWPBPL32xdkcC5SmULWmorY2YvDQ3MQq2Vwsd+/KcTmiGO+rzVfC8pQaozSg4pUWURNf8hs+TuV9R1rpFSWPz1EbNwaofYRFwYbmyIOUzRqAhp/QEtF4RsViU+gSaR6O3wiqrtI88GGPwKNuE0EpFyj5DY6DfY5sj9X2zcO2Aq8hVZzKtxmuJp1PaYrauC0Bb5PwKg6bTSXwUPiNxQwrLEzMx9RvB9VfyL3g9+Nqs4/trUTNhZ9zFKuzdpzFDKrGkm1A7xOTy6f0NyxsETw3tnP4Hfc9Q+3i7CR67nZjfXiN2B4Dq/HJ9dUbp2PDp+nYdPW7vvddvxeo9ZXFnQov6JJF8FYIb6xqNiN7gfNim6Lo2xs0f76sr7QxmaLGZOyqg9lF5C7qFaddd7oxxfmcosYk2IHUPiwvmYabae3toP+TpJ2vw67PvE/r91vGIFd7x4EDaf0z2pLxyX37o8+biXwxst2bdX/1+Q93knlZQubovAAAAABJRU5ErkJggg==>

[image8]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAQCAYAAAAFzx/vAAAAmUlEQVR4XmNgQAX/oZgHyg+F8lfBVVAZwCykG6CrZSBAVwtvMCCClC5Bi24JXSykG4hkwG0hLnGKAHpwwgA2MXLBbBgDPaGgY2oBappFFCDbQphG5BBAD41tSOIwQJGF75DYMLAXSn9DEkN2ENkAm6tfo4mhW4DOJwm8hNIFSGLYHIEMsIkRBZ4isdEtEUVii0NpGACxZUEMAMc0P2tcvHRFAAAAAElFTkSuQmCC>

[image9]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJwAAAAjCAYAAABhJGPtAAADrElEQVR4Xu2cMaxMURCGT6EQEQ0iqqdWaERHXiSiUIiSQhQStYhEISoFhUK0CpVIRCEieqUQUYhWIQqRiIiIRMGOd2Z37v9mzj1n9l5v95kvOdnz/zNz3tm7s3v37i4pBWPze6ARBNVg83hGEDQhm+cDxEpEwwVuZNPt64ZMTqVouMCJ9zTZkhsEHTxNV5u3aDxMbfczGAlP0y0b28V8axrgfj5AI6jmfeo23JZu2MXcD6hBy7oy95GYE8V18BmoPRNRLxranmvx1rVQOrYetDWstdFDzZAvX6kQrEMtUWNHkx7Yk7o+zenqaZGxDnYN3rpWeI/z7JXR6rV1UROaR1g+g3HUzGs0iAPJLkBq8zYS7WDX4q1r5XTqNtzLbrgJa8/kXxNzjVafwTjqIpR8Hk0DuTDN9wp9KHsMbmI1e+ifER6+ybwEWsJrPZ6MFcW3KMUtfwx4HzQOQ6wFa8+89rPJ2A0xRqs9kmb+UzEkWIcamb7v/5r6k5ljaX1uSVtz1HxgpH41GfeFltxKa43JYBzXY45PxkGhtRzL6xte5q0nSvUUe4KmQKsl70qen5ABAdZpWj0+64wClLcK+qLQJ7O3U3iEtr70ME56G2jmJmhC0+hZ71GRmpyh0PbpobRG39/QYuxpMQZjqE36NiTBXKwjrb1JxDwC19kPmqFTAeZK6GMF9HCf7NErXB9YNxbaHr1Y65B/Od9aaLGavWEctUnN4gzm9WlCW7/URFdB0/xNnu+AGEGaTrHoaXk1aHm8Xmm0QF/gU80Qn8ER2t+XnhZnMPZJeBiTYAy1yZ1Ul4wHlq5+sA41gXXsyflt0BLW5/Ica1l/NHzp1VCb54W/kB/yoyXcs6bRY9DH42uBMdRFtA19AY1xrqErGkJe2SClO1GjL4Beybes783CU09bh73Sg411Q6PtrY9daAByPZq/EJp4nn0N9KV+l/Vb4TGlumroauZH6n7UsYx4HlTGW1eDZ1+/0BiY1v0w3rpNieeBZbx1fXj35Klpwbu+t25Twg9uy4Pcmt/CjbS2bt+pERlrP5LW+92aH2wA+ARoHUFQDTZP67iegqASbB7PCIIgCILgL9avLYJgFOJ9WPDPqLnCpG935EXC5244COrhV7e7eUjo+87WVz/60ek3NIOA4YbSGkvzSnA+/TD1pwwEAUO/uLEaCz9vK51SrTWCYMrZfGs1i+VrtOQG/yncJN877oyWJpK58t96BMEU2SRWc+Hp1Dql0n+dwPGl5Q/PvvDPyFygfwAAAABJRU5ErkJggg==>

[image10]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAASgAAAAQCAYAAAClWeJtAAAErUlEQVR4Xu2bT6gNURzHJ1lIUrKQhZQkWdhZSXaWkpKFJClJspWkl72VpGTxkqQkSZKNhYWkLCRJSrKQpCQLSYr77Z1f73u/73fOnDP3znPvm/nUdM/3e37nz5wzc2fOzL1V1bOUWafGIvM3bKXsU6OjbFCjJe5Ww/N0SXRbrFYjB3TskXiPg98zHXxRI4HOK/Qr8UZB6y9hRo0OkTNuqQtAzPdA7C/Sa4O3GGS3s6xKB39SY0SWqzFm3qvREXBxyb1z8g5wz2sK6rmpZgGHB9sKNTtA7vjH5srzUmg89HHx2uSDGh6xnR03q6p22jlJ6cXal0mkZL+9cfK8poyjnnHUMW3k7vP3yo89q0YNWofqtqltL7ajMTh2VjRuFVkjzbePWHdqW9DrwyfnvRtsZ0h75erSJVj7qU25Us37tg8/BtvL4HllUn3VPNUXBtsx0sw2x0uhsdoewBxcD2kvr8n8lNC0XAnWhi2NTeunsYk8rDx+U17umFgZL1+9FBqrGrCH44f1OdFANWBP00dEl4Iyl9VkSgZF43RpiDQ81vtF46RmNAbcCz6T0qcorXFtgrbOV/NLEW07pXFh0Ds/plT/dLwY3vh6cAynvfKsD5HWuBJQFidVm6CNzaLxRcOaaTomdq7Eypt+KF4KLu89htH68Tz5NWnk7yL9JHgMaz1md1fD+bhIlqJjsoDagABi+GoBvgXfQJrfwmi9qkGOhy8B9bwDAnheW6CtGdEG7nR0bDB+3jIX+oDjlWr1YuTEWv6zauFJo2V1fpC+IV4TUP6BmsLXan5/YlsKzsec/SGt5ZHGQ2SdW8tjvDHhZ3LQt0ibh+M6F8TbF4x+OWjfzSvVsWPWYP8opXPx+jlEbUDAi2Fvr2hQp/EwWz2vP6oNjUX6NOkSrK7UprC3UjTST0XH0DxtTzWulvqiwTtpYuTExWK0L+Z5Gp/bOaMQlN+h5hhB/bOidQXAqDZKxiSmgVdPCov3yqinyztQqj0sBndfTYj1f4hYwCylNeZjNXd1NZCv6297fgFeBI+B1hNNO4zbbdNvB9tBygMca2ltpw3QBq7erLlv1geL0T6toTTn4Q4U+ip5Wja2n6o99MoeQ2O4Tc7T+QGcb+kT5OWifRg3Wn9MfxBt3A+fpWPCmu86NpKfg7bLqL9VPKT5Asr5W8Kn1sHHrHGnmnvu2hS0wReFKLaztvHJZ1iHteNAPR081eZ5WKy9Mkf6ouRZmvHaYPT51yhoO55mz+4w1Qfqa0wsXvE8xk6cWHkGB53F4QUAY35sfmZC2nSsrZhv1OWPCtevJzCAvk2axwRLWKZuTLzlHI+ToX1IoRdrxvpj9enLMM4Dz4PeQ17qmGV0LBh+SeaRqrdTdGUgpmk/vYugMU37MW6mad/r+prKT+V1DhsMfI7zTmoSmaaJ967OqrvIKD9ybRt7a/15yPXBXGLJqHP6RnTnwTMzQwerZ/HBHPDSUd8Q90wueNOY8yv/a9XC5X6PAw5+/gtIP1D/H54DPBvLelDaM1XoeTbKw/QlDQ9Uzm1pT/vgN3SGHsg9SwOe136OE9jg9IM0Geys5p5B4M/No/xOqmeysWV8o/PuH3A4HGyCwFOEAAAAAElFTkSuQmCC>

[image11]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAQCAYAAABk1z2tAAAA3klEQVR4Xs2TsQ3CMBBFLQoKBqFmATagYAEKRqGnRKyAxApZJEJiADaggzuE4efrcsS2RPykU3w/9r+vyAnhf7RSj3dlwwY76ksp9uKAUduSlgt7J2MZWFouxV5s0PdFrTX3fFbXDfR7WA8iGl6l7lLr7usXOHBKvRcW+0NHTUAN5iwCx/Ados8lvLtJXaBXrICsJfHrsDeA9QVpeJb3DsIbHvH2sD6TOkPPYZNYBX84EvfxXtb1DnuhLA9F7/2GxZqwQldFDNj3hUdlInWCvrqAHIj70fF+qirA+/fhCWGKVLJyeh0LAAAAAElFTkSuQmCC>

[image12]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADAAAAAQCAYAAABQrvyxAAABA0lEQVR4XtWSsQ3CMBBFXbEEC1CxAg01GyDEAlQsQMsSVIiOgiVYgIoGUdJSUCGBT4rR19M5BJQI8qRT/L/vzj7FIdTLNsYjxrLQs0JbNE7ZQTnfg7mmbbDGyQ3geWUwn7oxVsE/rEejhE2MOzyvZ2PwMGpDPe5TLxwvV3+FZl0ltOgk6wSbfqPX0Ar1x2iDsawNr7l6Q2gjp28x9rpRoPmsrYQV2Rv2iumZHkHvRHcLL2Fr9iApp8ONqpxD/pDcZfi9iLZ+CW+AAbTBnNpIF9AL54bytHoWfewlWEP4tP+KCQ3wbri/J/f3f8o8VL8Mn2irOMaYim7dAHrhg6xbg77/F08rU2czz17/dwAAAABJRU5ErkJggg==>

[image13]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAG8AAAAsCAYAAABrCeaiAAACSklEQVR4Xu2cv0rEQBDGFxGxEDvxDSzFTkTERiwsxEbEQq4QRHwDK9/CxlpsRCzsLCzFVxAsLMTCRkRERNAM7nhzQ/aSM8lm1/1+MOy3k3+TnWw2ySVnTHzcZfZljZG6Dnj9vN45oUENcGOO9XjrBQlrCN37NLL3uKwImmdGO0F1Nky5BFSB1j+unaA6m6b55A2Z5reRHO+25IY95Ak1Mm1L3sZfkric2bF2pooeq3S9DvQ6dX1QqPcCAOqgY35646Qt5anV1WtZs93wTMA/Mkl6XNMJLNLAM7Lxt4UmXElyaeAZJC9iZOPvCE24kuTSjeN1Y6BekLyIQfIi5k07QBh0bKkHVH3/AgKGkzfV4+0PLVNkZ79zg8Y4N/7GNp1gWHlz0nciCJcjM3jy9FGRZzhtNgwnjUv6pRoEjj6Pvqo6AAAAAAAAALSM/OViUejQOVD1D1VPAr6/vMpsNrNRMS1k6GMUjv1S6KSgnV7Szkig2F+0MyVGTDtHLT9l6mdFlJnnX1O2oUKE4h7WztSIMXkUM12kxBh7JXiH+SNGqtPFSgwNQe9ryjirxEzL6vc/AQiDVVvK+6i8t9pCvc+6yGzF6t3MTsU0YkHoR1s+CF/UuE5RrKkxTpSPNb2fsy98PtGxMM+ZrQv/ltXyc+oJoaOGjlzG1SCM9lG9rT8HcMW6ZrqfaD+ZbvII1zLRUiZ5rPUOU137fJEXH4HkCZ3nI66F71b4feGKK5nk7Rn3DrH+tFoaMW9Loo2G0LHyM1uOl/2s74WmcTw35m9vwTIEDNE5bwAAAABJRU5ErkJggg==>

[image14]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABwAAAAMCAYAAABx290PAAAAkElEQVR4XmNggIBQIP4BxP+hfBAAsZci8WkCYBaqoYjSEIAsRPYlzQHdLQQBmlsIssAPjf8QiU8qoLmDaQaCGBCuB9HiSGwYiEXiayGxQfQVKJskcBxKVwOxI5SNbGEJELci8UFyfUhskgBIQy0SG1kcFxvG/4MkTjRAN4xcNtFgG5ROA2JZJHFcBqOz3UAMAL1WLuq61EqDAAAAAElFTkSuQmCC>

[image15]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAB0AAAAMCAYAAACeGbYxAAAAmklEQVR4XmNggIBQIP4PxTCAzKYpoJtFyABkqR+6IK0BehDTHOyG0nSxFD1IQXwtJP7IA+sYMKPgAhIbBkD8T0jirUhsEG0NZRMF0PMwyGB08Uok9mskNkhNHhKfaIBuKQhEAnE4mhgI/EFigwDIt2xoYkSBl1C6AIjVoGxsDkFnwwA2MbzgKRIb3fBLSGzkuIPRS5HYoHTBAABdLjEkRpAdbAAAAABJRU5ErkJggg==>

[image16]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJAAAAAoCAYAAAAR33OgAAADi0lEQVR4Xu2bMYsUQRCFGzEwMBNDEyNDQYxERDAQ/4GBiJiIf8BIjMzEwEAwFDETAxETg4vMxMhATAwMDAQxEBERdMud8nrfVb/u3il39+bqg+a63ut5s2z17e7NzqUUbDq/UVgSyZFxZjYuDPOPCyuCyfEm+W8g1IIJcyX5NTk20B5Dm+vVZMx5b2jBRDiczaXJ8pllDD/TPOfgbFwa5q8XVgST4k42t956cpinYMZ3qIMJ8SxtNzwfJcR7iSIga04bGssNdinWn9ZjG20dHxtogpQaWtJbsDbKdUMLdjnPU7mposuf9MuAG2hrqPdlWhBMm3MoVLiBQiP626bj86L9l/MoBJvNNxQqfE3ll/IW8CUba+EU1MGG8nY2DqFYwWp4D9bxWAuWFoxkazYeoTjwNM1fHSzEe4di6m+SrL8//FwWPPasoQlX0/xyfuDAg7Tz8rnyYTZuZ7V4ouW1NbfqVsYch8dKfRk0BdcGS4JPJNsUQs0X9IpqKy2ZNXQDHZuNH8OcvYW2nEcz2ZBX4D2LPgklLE+0V9lcxvFte0FvAa++ynGyAXqR4w5k9clBK8G8seAmm9r4xw4BsDzRvmS1fPmHOb+gZtyFGrNasY7Bx5pjrQ86uZnsJ/Lx8NPyLE0Q/SHUNaw1y2wg6xi52opaDvMUzWWj5S0sP1fLeRksi3k9dOXoE5HX+RwD8jq/r0T00odxi2soDJTuxLMei2J5lpbDPG/wOR0Dy2JeD905etPRPTTS/INoqRmqy8DvV6z1Sn5cSUdPLhWgJuAx8vnpxMKKnVg5/5P8fGPPzbKY14NXzmi8T+6VJzdVrRLPhrAs5vXgleOC1wPYtJwePBvCspjXg1dO4IRnQ1gW83rwygmc6G0IW8OymKeIjgNpyQlWSG9D2BqWxTwFNw3WqlnzYE30NEQbuh+NAZbFPAX1i4bWkhOskNaG6KbRTWTBspgnSD7q1rlqOcGKaW2I3BstWE1VWBbzBM2VfzJ8MsyPLqyYU8sJVkxLQ3L9E9Q5LIt5gmhHoC6ts+bBmmhpiDYzHxYsi3kCarcMTajlBCum1pBWTWBZNQ+10hfOLCdYA6whcu+4hazL/09eYVk1r0UTWE6wBlhDsFaWaW7Ny7UXUOewnGANeDaEZTGvB6+cwAnPhrAs5vXglRM44dkQlsW8HrxyAic8G8KymNeDV07ghGdDWBbzemjK+QOUwv9J+XFl1gAAAABJRU5ErkJggg==>

[image17]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAJCAYAAABT2S4KAAAAmElEQVR4Xp2TMQ6AIAxFG2Oc3B09hZMX8BbewdXZg3gJV4+mVKjBppTKS5rg4/NxASDNxUUhLfiu000V1qZuDA1cFkCXxmR/ggJqyIjUI7kX2lBDP8COg32beicwBhU68B2NmyWs1U4KxJMit49IGck9SBLdxuUP8PwuOOku6LkAJWxgBPksujUWc5D8ycVvtmZ7Fugsnw83Qc868RrsdL4AAAAASUVORK5CYII=>

[image18]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAD0AAAAUCAYAAAA+wTUXAAABR0lEQVR4Xq2TMW5CQQxEt6LnGtwhl+AoiB7lUmm5EUWKtIDRrrLMt8c7iZ+E1vYYM1PQ2i93eP/K/P3/3Kq+496gokC1WaxVaC4qClSbxVqF5qKiQLVZrFVoLioKVJvFWoXmoqJAtVmsVWguKgK2c8Rhp9os1jM4x96guagI2E60t2J2hezOZ9vOPV80FxUnxuFoLzO7SnbH82D9jzOb3zeo2Pno76XFe5nZVbI7NvuCPtqb3zeo2Jn/x9FeZnaV7I7Nds/PqdfejkFzUbFt59gPMrOrsDtXZxYFp7mo6GB7Bxw2blaB3fECejOD5mJiNIvmXq3C7mBvZH48LRS/oR9kP4L16G8wi4junKE3Ii9GlOsFFQUiswNv5pHdWYXmoqJAZnaPg4Dszio0FxUFqs1irUJzUVGg2izWKjQXFQWqzWKtssn1AKiY04dONavUAAAAAElFTkSuQmCC>