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

## **2.1. Nguyên tắc xây dựng bộ thuộc tính**

Mục tiêu của bộ thuộc tính là biểu diễn mỗi đoạn nhạc dưới dạng một vector số sao cho vector này phản ánh được các đặc điểm quan trọng của nội dung âm thanh. Đối với bài toán tìm kiếm bản nhạc tương đồng, vector đặc trưng cần mô tả được nhiều khía cạnh khác nhau của tín hiệu âm nhạc như nhịp điệu, năng lượng, dạng sóng, phổ tần số, âm sắc và hòa âm.

Một file âm thanh không nên chỉ được biểu diễn bằng một vector duy nhất cho toàn bộ file, vì tín hiệu âm nhạc thường thay đổi liên tục theo thời gian. Trong cùng một bản nhạc có thể tồn tại đoạn mở đầu nhẹ, đoạn cao trào mạnh, đoạn có nhiều nhạc cụ hoặc đoạn chỉ có một nhạc cụ chính. Nếu chỉ lấy một vector trung bình cho toàn bộ file thì nhiều thông tin cục bộ quan trọng sẽ bị mất.

Do đó, hệ thống sử dụng phương pháp chia file thành nhiều đoạn ngắn bằng cửa sổ trượt. Mỗi đoạn âm thanh được trích xuất một vector đặc trưng riêng. Khi tìm kiếm, file truy vấn cũng được chia thành nhiều đoạn tương tự, sau đó so sánh các đoạn truy vấn với các đoạn trong cơ sở dữ liệu. Cách làm này giúp hệ thống tìm được các bản nhạc tương đồng ngay cả khi file truy vấn chỉ là một phần ngắn của bản nhạc.

Trong hệ thống demo, mỗi file âm thanh có độ dài khoảng 30 giây. Hệ thống sử dụng:

- Độ dài cửa sổ: `W = 5 giây`.
- Bước trượt: `H = 2,5 giây`.
- Độ chồng lấn giữa hai cửa sổ liên tiếp: 50%.

Số đoạn được tạo từ một file âm thanh có thời lượng `T` được tính theo công thức:

```text
Số đoạn = floor((T - W) / H) + 1
```

Trong đó `T` là thời lượng file âm thanh, `W` là độ dài cửa sổ và `H` là bước trượt. Với `T = 30`, `W = 5`, `H = 2,5`, số đoạn là:

```text
Số đoạn = floor((30 - 5) / 2,5) + 1 = 11
```

Như vậy, một file âm thanh 30 giây tạo ra khoảng 11 vector đặc trưng. Nếu bộ dữ liệu có 1000 file thì tổng số vector đoạn xấp xỉ 11000 vector.

## **2.2. Lý do sử dụng mean và std**

Nhiều đặc trưng âm thanh như RMS, ZCR, Spectral Centroid, MFCC, Chroma hay Spectral Contrast không chỉ tạo ra một giá trị duy nhất, mà tạo ra một chuỗi giá trị theo nhiều frame thời gian trong một đoạn âm thanh. Để biểu diễn chuỗi giá trị này thành vector cố định, hệ thống sử dụng hai thống kê cơ bản:

- **Mean**: giá trị trung bình, biểu diễn mức đặc trưng tổng quát của đoạn âm thanh.
- **Std**: độ lệch chuẩn, biểu diễn mức biến động của đặc trưng theo thời gian.

Việc dùng cả mean và std giúp vector giàu thông tin hơn. Hai đoạn nhạc có thể có cùng mức năng lượng trung bình nhưng độ biến động năng lượng khác nhau; hoặc có cùng độ sáng phổ trung bình nhưng một đoạn ổn định, đoạn còn lại thay đổi mạnh theo thời gian. Nếu chỉ dùng mean thì các trường hợp này khó phân biệt. Std giúp mô tả cấu trúc biến thiên của âm thanh, từ đó cải thiện khả năng tìm kiếm tương đồng.

Ví dụ:

- `RMSMean` cao cho biết đoạn nhạc có năng lượng lớn.
- `RMSStd` cao cho biết năng lượng thay đổi mạnh, có thể có cao trào hoặc tiết tấu rõ.
- `SpectralCentroidMean` cao cho biết âm thanh sáng.
- `SpectralCentroidStd` cao cho biết độ sáng âm thanh biến thiên nhiều theo thời gian.

## **2.3. Thuộc tính trên miền thời gian**

Miền thời gian biểu diễn trực tiếp sự thay đổi biên độ của tín hiệu âm thanh theo thời gian. Các thuộc tính trong miền này giúp mô tả năng lượng, mức dao động và nhịp điệu của đoạn nhạc.

### ***2.3.1. Tempo***

**Khái niệm:** Tempo là nhịp độ của bản nhạc, thường được đo bằng BPM, tức số nhịp trong một phút.

**Cách tính tổng quát:**

```text
BPM = số nhịp × 60 / thời gian
```

Trong hệ thống, tempo được ước lượng dựa trên các điểm onset, tức các thời điểm xuất hiện sự kiện âm thanh mới. Nếu khoảng cách trung vị giữa các onset liên tiếp là `d` giây, tempo có thể được xấp xỉ:

```text
Tempo = 60 / d
```

**Lý do lựa chọn:** Tempo là đặc trưng quan trọng trong cảm nhận âm nhạc. Các bản nhạc có phong cách tương tự thường có nhịp độ gần nhau, ví dụ nhạc thư giãn thường chậm hơn nhạc dance hoặc nhạc sôi động.

**Giá trị thông tin:** Tempo giúp phân biệt nhạc nhanh, nhạc chậm, nhạc nhẹ nhàng và nhạc có tiết tấu mạnh.

**Ví dụ:** Một bản nhạc dance, EDM hoặc hip-hop sôi động thường có tempo khoảng 110–140 BPM, tạo cảm giác nhanh và mạnh. Ngược lại, một đoạn piano thư giãn, nhạc nền nhẹ hoặc ballad không lời thường có tempo khoảng 60–80 BPM, tạo cảm giác chậm và êm hơn. Khi người dùng đưa vào một đoạn nhạc có tempo nhanh, hệ thống có thể ưu tiên các bản nhạc trong cơ sở dữ liệu có nhịp độ tương tự.

### ***2.3.2. OnsetMean, OnsetStd và OnsetDensity***

**Khái niệm:** Onset Strength đo mức thay đổi năng lượng phổ tại thời điểm xuất hiện sự kiện âm thanh mới như tiếng trống, tiếng gảy guitar hoặc một nốt nhạc mới.

Hệ thống sử dụng ba thuộc tính:

- `OnsetMean`: cường độ onset trung bình trong đoạn.
- `OnsetStd`: mức biến động của onset strength.
- `OnsetDensity`: mật độ onset trong một giây.

**Công thức onset density:**

```text
OnsetDensity = số lượng onset / thời lượng đoạn âm thanh
```

**Lý do lựa chọn:** Nhóm thuộc tính này mô tả rõ cấu trúc tiết tấu của đoạn nhạc. Một đoạn có nhiều tiếng gõ, nhiều nốt tách bạch hoặc nhịp nhanh thường có onset density cao. Ngược lại, nhạc nền kéo dài, ambient hoặc piano nhẹ có thể có onset density thấp.

**Giá trị thông tin:** OnsetMean và OnsetStd cho biết độ rõ và độ biến động của nhịp; OnsetDensity cho biết mức dày đặc của sự kiện âm thanh. Ba thuộc tính này hỗ trợ tốt cho việc tìm các đoạn nhạc có tiết tấu tương đồng.

**Ví dụ:** Một đoạn nhạc có tiếng trống rõ, guitar gảy liên tục hoặc piano đánh từng nốt tách bạch thường có `OnsetDensity` cao vì xuất hiện nhiều sự kiện âm thanh trong một khoảng thời gian ngắn. Nếu các tiếng gõ có cường độ không đều, lúc mạnh lúc nhẹ, `OnsetStd` cũng sẽ cao. Ngược lại, một đoạn pad synth kéo dài, violin legato hoặc nhạc ambient thường có ít điểm onset rõ ràng nên `OnsetDensity` và `OnsetMean` thấp hơn.

### ***2.3.3. RMSMean và RMSStd***

**Khái niệm:** RMS Energy biểu diễn năng lượng hiệu dụng của tín hiệu trong một frame thời gian.

**Công thức:**

```text
RMS = sqrt((1/N) × Σ x[n]^2)
```

Trong đó `x[n]` là giá trị biên độ của mẫu âm thanh và `N` là số mẫu trong frame.

Hệ thống sử dụng:

- `RMSMean`: năng lượng trung bình của đoạn âm thanh.
- `RMSStd`: độ biến động năng lượng theo thời gian.

**Lý do lựa chọn:** RMS phản ánh độ mạnh/yếu của âm thanh. Những đoạn cao trào hoặc nhiều nhạc cụ thường có RMSMean cao; những đoạn mở đầu nhẹ hoặc ít nhạc cụ thường có RMSMean thấp.

**Giá trị thông tin:** RMSStd giúp phân biệt đoạn nhạc có năng lượng ổn định với đoạn có năng lượng thay đổi mạnh. Điều này quan trọng vì hai đoạn có âm lượng trung bình tương đương nhưng cấu trúc năng lượng khác nhau có thể tạo cảm giác nghe rất khác nhau.

**Ví dụ:** Một đoạn cao trào có nhiều nhạc cụ cùng chơi như trống, bass, piano và strings thường có `RMSMean` cao vì năng lượng tổng thể lớn. Nếu đoạn nhạc chuyển từ phần nhẹ sang phần mạnh hoặc có nhịp trống nổi bật theo từng nhịp, `RMSStd` sẽ cao do năng lượng biến động nhiều. Ngược lại, một đoạn nhạc nền đều, âm lượng ổn định có thể có `RMSStd` thấp dù `RMSMean` không quá thấp.

### ***2.3.4. ZCRMean và ZCRStd***

**Khái niệm:** Zero Crossing Rate là tỷ lệ số lần tín hiệu đổi dấu từ dương sang âm hoặc từ âm sang dương trong một frame.

**Công thức:**

```text
ZCR = (1 / 2N) × Σ |sign(x[n]) - sign(x[n-1])|
```

Trong đó `x[n]` là mẫu tín hiệu tại thời điểm `n`, `N` là số mẫu trong frame.

Hệ thống sử dụng:

- `ZCRMean`: mức đổi dấu trung bình.
- `ZCRStd`: độ biến động của mức đổi dấu.

**Lý do lựa chọn:** ZCR phản ánh mức dao động nhanh của tín hiệu. Âm thanh sắc, nhiều thành phần cao tần hoặc tiếng gõ thường có ZCR cao; âm thanh trầm, mềm thường có ZCR thấp.

**Giá trị thông tin:** ZCR hỗ trợ phân biệt âm thanh sáng/sắc với âm thanh trầm/mượt, đồng thời bổ sung thông tin cho các thuộc tính phổ.

**Ví dụ:** Một đoạn nhạc có nhiều tiếng hi-hat, tiếng gảy guitar nhanh hoặc percussion sắc thường có `ZCRMean` cao vì tín hiệu dao động và đổi dấu liên tục. Trong khi đó, đoạn nhạc có bass trầm, cello hoặc piano ngân dài thường có `ZCRMean` thấp hơn. Nếu đoạn nhạc xen kẽ giữa phần trầm và phần có nhiều âm sắc sắc, `ZCRStd` sẽ tăng do mức đổi dấu thay đổi theo thời gian.

## **2.4. Thuộc tính trên miền tần số**

Miền tần số biểu diễn tín hiệu âm thanh sau khi biến đổi sang phổ tần số. Các thuộc tính miền tần số giúp mô tả độ sáng, độ rộng phổ, vùng năng lượng chính và độ phức tạp của phổ âm thanh.

### ***2.4.1. SpectralCentroidMean và SpectralCentroidStd***

**Khái niệm:** Spectral Centroid là trọng tâm của phổ tần số, cho biết năng lượng phổ tập trung nhiều ở vùng tần số thấp hay cao.

**Công thức:**

```text
Centroid = Σ f[k] × |X[k]| / Σ |X[k]|
```

Trong đó `f[k]` là tần số tại bin `k`, `|X[k]|` là biên độ phổ tại bin đó.

**Lý do lựa chọn:** Spectral Centroid phản ánh độ sáng hoặc độ tối của âm thanh. Nhạc có nhiều cymbal, violin cao hoặc âm thanh sắc thường có centroid cao; nhạc có bass hoặc âm trầm thường có centroid thấp.

**Giá trị thông tin:** Mean cho biết độ sáng trung bình, còn std cho biết độ sáng thay đổi ổn định hay biến động trong đoạn.

**Ví dụ:** Một đoạn nhạc có nhiều cymbal, violin ở quãng cao hoặc âm thanh synth sáng thường có `SpectralCentroidMean` cao vì năng lượng tập trung nhiều ở vùng tần số cao. Ngược lại, đoạn nhạc có bass, cello hoặc âm nền trầm thường có centroid thấp. Nếu đoạn nhạc liên tục thay đổi giữa phần trầm và phần sáng, `SpectralCentroidStd` sẽ cao, phản ánh sự biến đổi âm sắc theo thời gian.

### ***2.4.2. SpectralBandwidthMean và SpectralBandwidthStd***

**Khái niệm:** Spectral Bandwidth đo độ phân tán của phổ tần số quanh Spectral Centroid.

**Công thức tổng quát:**

```text
Bandwidth = (Σ |X[k]| × |f[k] - Centroid|^p / Σ |X[k]|)^(1/p)
```

Thông thường `p = 2`.

**Lý do lựa chọn:** Spectral Bandwidth cho biết phổ âm thanh rộng hay hẹp. Đoạn nhạc có nhiều nhạc cụ, nhiều lớp âm thanh thường có bandwidth cao; đoạn chỉ có một nhạc cụ đơn giản thường có bandwidth thấp hơn.

**Giá trị thông tin:** Mean mô tả độ rộng phổ trung bình, std mô tả mức thay đổi của độ rộng phổ theo thời gian.

**Ví dụ:** Một đoạn nhạc phối khí dày, có trống, bass, piano, guitar và strings cùng xuất hiện thường có phổ trải rộng nên `SpectralBandwidthMean` cao. Ngược lại, đoạn chỉ có một nhạc cụ đơn giản như sáo hoặc piano đơn âm thường có phổ hẹp hơn. Nếu bản nhạc thay đổi từ phần ít nhạc cụ sang phần nhiều nhạc cụ, `SpectralBandwidthStd` sẽ tăng do độ rộng phổ thay đổi rõ rệt.

### ***2.4.3. SpectralRolloffMean và SpectralRolloffStd***

**Khái niệm:** Spectral Rolloff là tần số mà dưới nó chứa một tỷ lệ năng lượng phổ nhất định, trong hệ thống sử dụng tỷ lệ 85%.

**Công thức tổng quát:**

```text
Σ từ 0 đến f_rolloff |X[k]| = 0.85 × Σ toàn phổ |X[k]|
```

**Lý do lựa chọn:** Spectral Rolloff giúp mô tả vùng tần số chứa phần lớn năng lượng. Nếu rolloff cao, âm thanh có nhiều thành phần cao tần; nếu rolloff thấp, năng lượng chủ yếu tập trung ở vùng thấp.

**Giá trị thông tin:** Rolloff bổ sung cho Spectral Centroid trong việc phân biệt âm thanh sáng/tối và mức hiện diện của thành phần cao tần.

**Ví dụ:** Một đoạn nhạc có tiếng cymbal, hi-hat hoặc âm synth sáng thường có `SpectralRolloffMean` cao vì cần vùng tần số cao mới chứa đủ 85% năng lượng phổ. Ngược lại, đoạn nhạc bass trầm hoặc piano nhẹ ít cao tần thường có rolloff thấp hơn. Nếu đoạn nhạc có lúc xuất hiện nhiều nhạc cụ cao tần, có lúc chỉ còn nền trầm, `SpectralRolloffStd` sẽ cao.

### ***2.4.4. SpectralContrastMean và SpectralContrastStd***

**Khái niệm:** Spectral Contrast đo sự khác biệt giữa các đỉnh phổ và đáy phổ trong từng dải tần số.

**Công thức tổng quát:**

```text
Contrast_b = mean(Peak_b) - mean(Valley_b)
```

Trong đó `Peak_b` là nhóm giá trị phổ lớn nhất và `Valley_b` là nhóm giá trị phổ nhỏ nhất trong dải tần `b`.

Hệ thống sử dụng 7 dải tần, do đó có:

- `SpectralContrastMean_1` đến `SpectralContrastMean_7`.
- `SpectralContrastStd_1` đến `SpectralContrastStd_7`.

**Lý do lựa chọn:** Spectral Contrast thể hiện độ tương phản và độ phức tạp của phổ âm thanh. Nhạc có nhiều lớp âm thanh, phối khí phức tạp thường có contrast khác với nhạc đơn giản hoặc ít nhạc cụ.

**Giá trị thông tin:** Nhóm này giúp hệ thống phân biệt độ dày, độ rõ và mức phức tạp của phối khí trong từng đoạn nhạc.

**Ví dụ:** Một đoạn nhạc có giai điệu piano nổi bật trên nền strings và trống thường có sự chênh lệch rõ giữa các đỉnh phổ và đáy phổ, làm Spectral Contrast ở một số dải tần cao hơn. Ngược lại, một đoạn nhạc nền đều, âm thanh trải phẳng hoặc ít nhạc cụ thường có contrast thấp hơn. Nếu phối khí thay đổi liên tục, chẳng hạn lúc chỉ có piano, lúc thêm trống và strings, các giá trị `SpectralContrastStd` sẽ phản ánh sự biến động đó.

## **2.5. Thuộc tính trên miền cepstral**

### ***2.5.1. MFCCMean và MFCCStd***

**Khái niệm:** MFCC là các hệ số cepstral trên thang Mel, mô phỏng cách tai người cảm nhận tần số âm thanh. Đây là một trong những đặc trưng phổ biến nhất trong nhận dạng âm thanh.

**Quy trình tính MFCC tổng quát:**

1. Chia tín hiệu thành các frame ngắn.
2. Tính phổ tần số của từng frame.
3. Đưa phổ qua các bộ lọc Mel.
4. Lấy log năng lượng Mel.
5. Áp dụng biến đổi Cosine rời rạc DCT để thu được các hệ số MFCC.

**Công thức tổng quát:**

```text
MFCC_i = DCT(log(E_mel))_i
```

Trong đó `E_mel` là năng lượng sau khi đi qua các bộ lọc Mel.

Hệ thống sử dụng 13 hệ số MFCC. Với mỗi hệ số, hệ thống lấy cả mean và std:

- `MFCCMean_1` đến `MFCCMean_13`.
- `MFCCStd_1` đến `MFCCStd_13`.

**Lý do lựa chọn:** MFCC mô tả âm sắc và cấu trúc phổ của âm thanh. Cùng một giai điệu nhưng chơi bằng piano, guitar hoặc violin sẽ tạo ra MFCC khác nhau.

**Giá trị thông tin:** MFCC giúp phân biệt chất âm, nhạc cụ, cách phối âm và màu sắc âm thanh giữa các bản nhạc.

**Ví dụ:** Cùng một giai điệu nhưng được chơi bằng piano và guitar sẽ tạo ra các hệ số MFCC khác nhau vì hai nhạc cụ có cấu trúc phổ và âm sắc khác nhau. Một đoạn nhạc orchestral với nhiều lớp strings, brass và percussion cũng sẽ có MFCC khác với đoạn acoustic guitar đơn giản. `MFCCMean` mô tả màu âm trung bình, còn `MFCCStd` cho biết âm sắc có thay đổi nhiều trong đoạn hay không.

## **2.6. Thuộc tính trên miền hòa âm và cao độ**

### ***2.6.1. ChromaMean và ChromaStd***

**Khái niệm:** Chroma biểu diễn năng lượng âm thanh theo 12 lớp cao độ tương ứng với 12 nốt nhạc trong một quãng tám: C, C#, D, D#, E, F, F#, G, G#, A, A#, B.

**Công thức tổng quát:**

```text
Chroma[c] = Σ |X[k]|² với k thuộc lớp cao độ c
```

Hệ thống sử dụng 12 giá trị Chroma. Với mỗi lớp cao độ, hệ thống lấy cả mean và std:

- `ChromaMean_1` đến `ChromaMean_12`.
- `ChromaStd_1` đến `ChromaStd_12`.

**Lý do lựa chọn:** Chroma phản ánh thông tin hòa âm, hợp âm và phân bố cao độ. Đây là đặc trưng phù hợp với nhạc không lời vì nhiều bản nhạc có thể tương đồng về vòng hợp âm hoặc giai điệu dù khác cách phối khí.

**Giá trị thông tin:** Chroma giúp hệ thống phát hiện các đoạn nhạc có cấu trúc hòa âm tương đồng, hỗ trợ tìm kiếm theo nội dung âm nhạc thay vì chỉ dựa vào âm sắc.

**Ví dụ:** Hai đoạn nhạc có cùng vòng hợp âm hoặc cùng giai điệu chính, dù một đoạn được chơi bằng piano và đoạn còn lại được chơi bằng guitar, vẫn có thể có phân bố Chroma tương đối giống nhau. Ngược lại, hai đoạn có hợp âm hoặc cao độ chủ đạo khác nhau sẽ có vector Chroma khác nhau. `ChromaMean` mô tả phân bố cao độ trung bình, còn `ChromaStd` cho biết các lớp cao độ có thay đổi mạnh theo thời gian hay không.

## **2.7. Bảng tổng hợp bộ thuộc tính đề xuất**

| Nhóm | Thuộc tính | Số chiều | Ý nghĩa chính |
| ----- | ----- | -----: | ----- |
| Nhịp điệu | Tempo | 1 | Nhịp độ BPM của đoạn nhạc |
| Nhịp điệu | OnsetMean, OnsetStd, OnsetDensity | 3 | Độ rõ, độ biến động và mật độ sự kiện âm thanh |
| Năng lượng | RMSMean, RMSStd | 2 | Mức năng lượng và độ biến động năng lượng |
| Dạng sóng | ZCRMean, ZCRStd | 2 | Mức dao động nhanh/chậm của tín hiệu |
| Phổ tần số | SpectralCentroidMean, SpectralCentroidStd | 2 | Độ sáng/tối của âm thanh |
| Phổ tần số | SpectralBandwidthMean, SpectralBandwidthStd | 2 | Độ rộng và mức phân tán phổ |
| Phổ tần số | SpectralRolloffMean, SpectralRolloffStd | 2 | Vùng tần số chứa phần lớn năng lượng |
| Phổ tần số | SpectralContrastMean_1..7, SpectralContrastStd_1..7 | 14 | Độ tương phản phổ theo từng dải tần |
| Cepstral | MFCCMean_1..13, MFCCStd_1..13 | 26 | Âm sắc, chất âm và nhạc cụ |
| Hòa âm/cao độ | ChromaMean_1..12, ChromaStd_1..12 | 24 | Hòa âm, hợp âm và phân bố cao độ |
| **Tổng** |  | **78** | Vector đặc trưng tổng hợp của một đoạn âm thanh |

## **2.8. Vector đặc trưng đề xuất**

Vector đặc trưng của một đoạn âm thanh được xây dựng theo thứ tự sau:

```text
Feature Vector = [
    Tempo,
    OnsetMean, OnsetStd, OnsetDensity,
    RMSMean, RMSStd,
    ZCRMean, ZCRStd,
    SpectralCentroidMean, SpectralCentroidStd,
    SpectralBandwidthMean, SpectralBandwidthStd,
    SpectralRolloffMean, SpectralRolloffStd,
    SpectralContrastMean_1, ..., SpectralContrastMean_7,
    SpectralContrastStd_1, ..., SpectralContrastStd_7,
    MFCCMean_1, ..., MFCCMean_13,
    MFCCStd_1, ..., MFCCStd_13,
    ChromaMean_1, ..., ChromaMean_12,
    ChromaStd_1, ..., ChromaStd_12
]
```

Số chiều của vector:

```text
1 + 3 + 2 + 2 + 2 + 2 + 2 + 14 + 26 + 24 = 78
```

Như vậy, mỗi đoạn âm thanh được biểu diễn bằng một vector đặc trưng 78 chiều. Vector này kết hợp thông tin từ nhiều miền khác nhau, giúp hệ thống so sánh nội dung âm thanh toàn diện hơn so với việc chỉ dùng một vài thuộc tính đơn lẻ.

## **2.9. Chuẩn hóa vector đặc trưng bằng L2 Normalization**

Các thuộc tính trong vector có thang đo rất khác nhau. Ví dụ, Spectral Centroid và Spectral Rolloff có thể có giá trị hàng nghìn Hz, trong khi RMS hoặc ZCR thường nằm trong khoảng nhỏ hơn nhiều. Nếu so sánh trực tiếp vector gốc, các thuộc tính có giá trị lớn có thể chi phối kết quả.

Để khắc phục vấn đề này, hệ thống chuẩn hóa vector bằng **L2 Normalization**:

```text
v_norm = v / ||v||₂
```

Trong đó:

```text
||v||₂ = sqrt(v₁² + v₂² + ... + vₙ²)
```

- `v` là vector đặc trưng gốc 78 chiều.
- `v_norm` là vector sau chuẩn hóa.
- `||v||₂` là độ dài Euclid của vector.

Sau khi chuẩn hóa L2, vector có độ dài bằng 1. Khi sử dụng cosine similarity, việc so sánh tập trung vào hướng của vector, tức cấu trúc tương đối giữa các thuộc tính, thay vì độ lớn tuyệt đối. Điều này phù hợp với bài toán tìm kiếm nhạc tương đồng vì hai đoạn nhạc có thể khác nhau về âm lượng nhưng vẫn tương đồng về nhịp điệu, âm sắc hoặc hòa âm.

L2 Normalization cũng có ưu điểm là không cần tính min và max của từng thuộc tính trên toàn bộ cơ sở dữ liệu. Khi có file truy vấn mới, hệ thống chỉ cần trích xuất vector 78 chiều và chuẩn hóa L2 trực tiếp, sau đó so sánh với các vector đã lưu trong cơ sở dữ liệu.

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
| track\_id | INTEGER | Mã định danh duy nhất của bản nhạc |
| title | TEXT | Tiêu đề bản nhạc lấy từ metadata crawl |
| source\_url | TEXT | Đường dẫn trang nguồn của bản nhạc |
| mp3\_url | TEXT | Đường dẫn file MP3 gốc |
| file\_name | TEXT | Tên file âm thanh |
| file\_path | TEXT | Đường dẫn lưu file âm thanh trong thư mục dữ liệu |
| duration | REAL | Thời lượng file âm thanh, tính bằng giây |
| format | TEXT | Định dạng file âm thanh |
| status | TEXT | Trạng thái file trong metadata, ví dụ `ok` |

### ***3.1.2. Thiết kế bảng track\_segments***

Bảng track\_segments dùng để lưu thông tin từng đoạn âm thanh sau khi file được chia bằng cửa sổ trượt. Mỗi đoạn có thời gian bắt đầu, thời gian kết thúc và vector đặc trưng tương ứng. Với file dài 30 giây, nếu dùng cửa sổ 5 giây và bước trượt 2,5 giây, mỗi file sẽ tạo khoảng 11 đoạn. Vì vậy, bộ dữ liệu có 1000 file, tổng số vector đoạn khoảng: 1000 × 11 \= 11000 vector.

**Cấu trúc bảng:** 

| Tên trường | Kiểu dữ liệu | Ý nghĩa |
| ----- | ----- | ----- |
| segment\_id | INTEGER | Mã định danh của đoạn âm thanh |
| track\_id | INTEGER | Mã file nhạc tương ứng |
| segment\_index | INTEGER | Thứ tự đoạn trong file |
| start\_time | REAL | Thời điểm bắt đầu đoạn, tính bằng giây |
| end\_time | REAL | Thời điểm kết thúc đoạn, tính bằng giây |
| tempo | REAL | Nhịp độ ước lượng của đoạn âm thanh |
| onset\_mean | REAL | Giá trị trung bình của onset strength |
| onset\_std | REAL | Độ lệch chuẩn của onset strength |
| onset\_density | REAL | Mật độ onset trong đoạn âm thanh |
| rms\_mean | REAL | Năng lượng RMS trung bình |
| rms\_std | REAL | Độ lệch chuẩn của RMS |
| zcr\_mean | REAL | Zero Crossing Rate trung bình |
| zcr\_std | REAL | Độ lệch chuẩn của ZCR |
| spectral\_centroid\_mean | REAL | Spectral Centroid trung bình |
| spectral\_centroid\_std | REAL | Độ lệch chuẩn của Spectral Centroid |
| spectral\_bandwidth\_mean | REAL | Spectral Bandwidth trung bình |
| spectral\_bandwidth\_std | REAL | Độ lệch chuẩn của Spectral Bandwidth |
| spectral\_rolloff\_mean | REAL | Spectral Rolloff trung bình |
| spectral\_rolloff\_std | REAL | Độ lệch chuẩn của Spectral Rolloff |
| rhythm\_features | JSON | Nhóm đặc trưng nhịp điệu gồm tempo, onset mean/std/density |
| energy\_features | JSON | Nhóm đặc trưng năng lượng RMS mean/std |
| waveform\_features | JSON | Nhóm đặc trưng dạng sóng ZCR mean/std |
| spectral\_features | JSON | Nhóm đặc trưng phổ gồm centroid, bandwidth, rolloff mean/std |
| spectral\_contrast\_mean | JSON | Mảng 7 giá trị trung bình Spectral Contrast |
| spectral\_contrast\_std | JSON | Mảng 7 giá trị độ lệch chuẩn Spectral Contrast |
| mfcc\_mean | JSON | Mảng 13 giá trị trung bình MFCC |
| mfcc\_std | JSON | Mảng 13 giá trị độ lệch chuẩn MFCC |
| chroma\_mean | JSON | Mảng 12 giá trị trung bình Chroma |
| chroma\_std | JSON | Mảng 12 giá trị độ lệch chuẩn Chroma |
| feature\_vector | JSON | Vector đặc trưng tổng hợp gốc gồm 78 chiều |
| normalized\_vector | JSON | Vector đặc trưng 78 chiều sau khi chuẩn hóa L2 |
| vector\_dimension | INTEGER | Số chiều của vector, bằng 78 |

	

## **3.2. Cơ chế trích xuất và lưu trữ metadata**

Quy trình trích xuất và lưu trữ siêu dữ liệu được thực hiện như sau:

1. Đọc file âm thanh và chuyển về tín hiệu mono.

2. Chia file thành các đoạn nhỏ bằng cửa sổ trượt 5 giây, bước trượt 2,5 giây.

3. Trích xuất các đặc trưng theo frame trong từng đoạn.

4. Tính mean và std cho các đặc trưng dạng chuỗi frame.

5. Ghép các đặc trưng thành vector tổng hợp 78 chiều.

6. Chuẩn hóa vector đặc trưng bằng L2 Normalization.

7. Lưu thông tin file vào bảng tracks.

8. Lưu vector đặc trưng gốc và vector đã chuẩn hóa L2 của từng đoạn vào bảng track\_segments.

Đầu tiên, hệ thống đọc file âm thanh và chuyển tín hiệu âm thanh thành chuỗi mẫu số. Sau đó, file được chia thành nhiều đoạn ngắn bằng cửa sổ trượt. Với file âm thanh dài khoảng 30 giây, hệ thống sử dụng cửa sổ 5 giây và bước trượt 2,5 giây. Như vậy, mỗi file tạo ra khoảng 11 đoạn âm thanh.

Với mỗi đoạn, hệ thống trích xuất các đặc trưng gồm Tempo, OnsetMean, OnsetStd, OnsetDensity, RMSMean, RMSStd, ZCRMean, ZCRStd, Spectral Centroid mean/std, Spectral Bandwidth mean/std, Spectral Rolloff mean/std, Spectral Contrast mean/std, MFCC mean/std và Chroma mean/std. Các đặc trưng này được ghép lại thành một vector đặc trưng tổng hợp gồm 78 chiều.

Sau khi tạo vector đặc trưng, hệ thống chuẩn hóa vector bằng phương pháp **L2 Normalization**:

```text
v' = v / ||v||₂
```

Trong đó:

- `v` là vector đặc trưng gốc 78 chiều.
- `||v||₂` là chuẩn Euclid của vector, được tính bằng:

```text
||v||₂ = sqrt(v₁² + v₂² + ... + vₙ²)
```

- `v'` là vector sau chuẩn hóa L2.

Việc chuẩn hóa L2 đưa các vector về cùng độ dài bằng 1. Khi đó, quá trình so sánh bằng cosine similarity tập trung vào hướng của vector, tức là cấu trúc tương đối của các đặc trưng, thay vì bị chi phối quá nhiều bởi độ lớn tuyệt đối của các giá trị. Phương pháp này phù hợp với bài toán tìm kiếm tương đồng nội dung âm thanh vì hai đoạn nhạc có thể có âm lượng hoặc cường độ khác nhau nhưng vẫn có cấu trúc phổ, âm sắc và hòa âm tương tự nhau.

Khác với Min-Max Normalization, L2 Normalization không cần tính giá trị nhỏ nhất và lớn nhất của từng thuộc tính trên toàn bộ cơ sở dữ liệu. Vì vậy, khi có file truy vấn mới, hệ thống chỉ cần trích xuất vector 78 chiều rồi chuẩn hóa L2 trực tiếp bằng chính vector đó. Điều này giúp quy trình tìm kiếm đơn giản hơn và không cần lưu thêm bảng thống kê min/max.

Cuối cùng, thông tin chung của file âm thanh được lưu vào bảng tracks, còn vector đặc trưng gốc và vector đã chuẩn hóa L2 của từng đoạn được lưu vào bảng track\_segments.

## **3.3. Cơ chế tìm kiếm bản nhạc tương đồng**

Khi người dùng đưa vào một file âm thanh truy vấn, hệ thống thực hiện các bước:

1. Nhận file âm thanh truy vấn

2. Đọc và tiền xử lý file truy vấn

3. Chia file truy vấn thành các đoạn nhỏ bằng cửa sổ trượt

4. Trích xuất vector đặc trưng cho từng đoạn

5. Chuẩn hóa vector đặc trưng của truy vấn bằng L2 Normalization

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