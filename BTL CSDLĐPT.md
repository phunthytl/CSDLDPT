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

## **1.1. Lý do chọn đề tài**

Âm nhạc là một trong những dạng dữ liệu đa phương tiện phổ biến nhất hiện nay. Số lượng file nhạc được lưu trữ trên các nền tảng trực tuyến ngày càng lớn, khiến nhu cầu tổ chức, lưu trữ và tìm kiếm âm thanh trở nên quan trọng. Trong nhiều trường hợp, người dùng không nhớ tên bài hát hoặc thông tin mô tả văn bản, nhưng lại có một đoạn âm thanh ngắn cần dùng để tìm các bản nhạc có nội dung tương tự.

Các phương pháp tìm kiếm truyền thống thường dựa vào tên file, tên bài hát, tác giả hoặc các thẻ mô tả. Cách tiếp cận này phụ thuộc nhiều vào metadata văn bản và không phản ánh trực tiếp nội dung âm thanh. Nếu metadata thiếu, sai hoặc không thống nhất, kết quả tìm kiếm có thể không chính xác. Vì vậy, cần xây dựng một phương pháp tìm kiếm dựa trên chính đặc trưng âm thanh của file nhạc.

Đề tài này tập trung xây dựng hệ thống lưu trữ và tìm kiếm bản nhạc tương đồng dựa trên nội dung âm thanh. Mỗi file nhạc được chia thành các đoạn ngắn, trích xuất vector đặc trưng và lưu vào cơ sở dữ liệu. Khi người dùng upload một file truy vấn, hệ thống trích xuất đặc trưng theo cùng quy trình, so sánh với dữ liệu đã lưu và trả về các bản nhạc giống nhất.

## **1.2. Mục tiêu đề tài**

Mục tiêu của đề tài là xây dựng một hệ thống demo có khả năng lưu trữ và tìm kiếm bản nhạc tương đồng bằng âm thanh. Hệ thống cần đáp ứng các yêu cầu chính sau:

1. Thu thập bộ dữ liệu gồm các file nhạc không lời có giai điệu cụ thể.

2. Xây dựng bộ thuộc tính đặc trưng để biểu diễn nội dung âm thanh của từng đoạn nhạc.

3. Thiết kế cơ sở dữ liệu SQLite để lưu thông tin file nhạc, vector đặc trưng và thông tin chuẩn hóa.

4. Xây dựng cơ chế tìm kiếm tương đồng dựa trên cosine similarity giữa các vector đặc trưng.

5. Xây dựng web demo bằng Flask cho phép người dùng upload file âm thanh và nhận về các bản nhạc giống nhất.

6. Hiển thị kết quả trung gian của quá trình tìm kiếm như số đoạn của file truy vấn, số đoạn trong cơ sở dữ liệu, số bản nhạc và thông tin cặp đoạn khớp nhất.

Trong phạm vi đề tài, hệ thống không sử dụng chỉ mục vector chuyên dụng. Việc tìm kiếm được thực hiện bằng cách quét tuần tự các vector đặc trưng đã lưu trong SQLite. Cách làm này phù hợp với quy mô demo và giúp minh họa rõ cơ chế so sánh tương đồng.

## **1.3. Bộ dữ liệu sử dụng**

Bộ dữ liệu được xây dựng bằng cách thu thập các bản nhạc không lời từ Pixabay Music. Đây là nguồn cung cấp nhiều file nhạc nền, nhạc không lời và hiệu ứng âm thanh phù hợp với yêu cầu của đề tài. Các bản nhạc được chọn có nội dung giai điệu rõ ràng, phù hợp để trích xuất đặc trưng âm thanh và so sánh tương đồng.

Quá trình thu thập dữ liệu được thực hiện bằng script crawler. Với mỗi bản nhạc, hệ thống lưu các thông tin cơ bản gồm:

- Tiêu đề bản nhạc.
- Đường dẫn trang nguồn.
- Đường dẫn file MP3 gốc.
- Đường dẫn file đã tải về trong thư mục dữ liệu.
- Thời lượng file sau khi xử lý.

Các file âm thanh không bị ép cố định đúng 30 giây. Khi tải dữ liệu, hệ thống ưu tiên cắt tại điểm lặng hoặc vùng âm lượng thấp gần mốc 30 giây để tránh làm đoạn nhạc bị ngắt đột ngột. Nếu không tìm được điểm cắt phù hợp, hệ thống có thể sử dụng fade-out ngắn ở cuối đoạn để giảm cảm giác bị cắt gượng. Vì vậy, thời lượng thực tế của mỗi file có thể dao động quanh mốc 30 giây.

Ngoài ra, crawler có cơ chế kiểm tra để tránh lưu nhầm file không phải âm thanh, ví dụ ảnh thumbnail hoặc nội dung HTML. Các bản nhạc gần trùng tên cũng được lọc bằng fuzzy matching để hạn chế tải nhiều phiên bản rất giống nhau của cùng một bản nhạc.

## **1.4. Phạm vi và công nghệ sử dụng**

Hệ thống được xây dựng ở mức demo cục bộ với các công nghệ chính:

- **Python**: ngôn ngữ chính để crawl dữ liệu, trích xuất đặc trưng, xây dựng database và xử lý tìm kiếm.
- **SQLite3**: lưu trữ metadata, vector đặc trưng và thống kê chuẩn hóa.
- **Flask**: xây dựng web demo cho phép upload file và hiển thị kết quả tìm kiếm.
- **Librosa, SoundFile, NumPy**: đọc file âm thanh, xử lý tín hiệu và trích xuất đặc trưng.
- **FFmpeg/FFprobe**: hỗ trợ kiểm tra, cắt và xử lý file âm thanh khi crawl dữ liệu.
- **RapidFuzz**: hỗ trợ lọc các bản nhạc gần trùng tên trong quá trình thu thập dữ liệu.

Hệ thống tập trung vào truy vấn tương đồng dựa trên nội dung âm thanh, không tập trung vào nhận dạng tên bài hát chính xác tuyệt đối. Đầu ra của hệ thống là danh sách các bản nhạc trong cơ sở dữ liệu có nội dung âm thanh gần giống nhất với file truy vấn, được sắp xếp theo độ tương đồng giảm dần.

# **PHẦN 2\. XÂY DỰNG BỘ THUỘC TÍNH NHẬN DIỆN BẢN NHẠC**

## **2.1. Nguyên tắc xây dựng bộ thuộc tính**

Mục tiêu của bộ thuộc tính là biểu diễn mỗi đoạn nhạc dưới dạng một vector số sao cho vector này phản ánh được các đặc điểm quan trọng của nội dung âm thanh. Đối với bài toán tìm kiếm bản nhạc tương đồng, vector đặc trưng cần mô tả được nhiều khía cạnh khác nhau của tín hiệu âm nhạc như nhịp điệu, năng lượng, dạng sóng, phổ tần số, âm sắc và hòa âm.

Một file âm thanh không nên chỉ được biểu diễn bằng một vector duy nhất cho toàn bộ file, vì tín hiệu âm nhạc thường thay đổi liên tục theo thời gian. Trong cùng một bản nhạc có thể tồn tại đoạn mở đầu nhẹ, đoạn cao trào mạnh, đoạn có nhiều nhạc cụ hoặc đoạn chỉ có một nhạc cụ chính. Nếu chỉ lấy một vector trung bình cho toàn bộ file thì nhiều thông tin cục bộ quan trọng sẽ bị mất.

Do đó, hệ thống sử dụng phương pháp chia file thành nhiều đoạn ngắn bằng cửa sổ trượt. Mỗi đoạn âm thanh được trích xuất một vector đặc trưng riêng. Khi tìm kiếm, file truy vấn cũng được chia thành nhiều đoạn tương tự, sau đó so sánh các đoạn truy vấn với các đoạn trong cơ sở dữ liệu. Cách làm này giúp hệ thống tìm được các bản nhạc tương đồng ngay cả khi file truy vấn chỉ là một phần ngắn của bản nhạc.

Trong hệ thống demo, các file âm thanh không bị ép cố định đúng 30 giây. Khi crawl dữ liệu, hệ thống ưu tiên cắt tại điểm lặng hoặc vùng âm lượng thấp gần mốc 30 giây để tránh làm đoạn nhạc bị ngắt đột ngột. Vì vậy, thời lượng thực tế của từng file có thể dao động quanh mốc này.

Hệ thống sử dụng:

- Độ dài cửa sổ: `W = 5 giây`.
- Bước trượt: `H = 2,5 giây`.
- Độ chồng lấn giữa hai cửa sổ liên tiếp: 50%.

Số đoạn được tạo từ một file âm thanh có thời lượng `T` được tính theo công thức:

```text
Số đoạn = floor((T - W) / H) + 1
```

Trong đó `T` là thời lượng thực tế của file âm thanh sau khi crawl/cắt, `W` là độ dài cửa sổ và `H` là bước trượt. Do `T` không cố định, số đoạn sinh ra từ mỗi file cũng không cố định.

Ví dụ, nếu một file có thời lượng xấp xỉ 30 giây thì số đoạn thường khoảng 11 đoạn. Nếu file dài hơn hoặc ngắn hơn, số đoạn sẽ thay đổi tương ứng theo công thức trên.

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

## **2.9. Chuẩn hóa vector đặc trưng bằng Z-score kết hợp L2 Normalization**

Các thuộc tính trong vector có thang đo rất khác nhau. Ví dụ, Spectral Centroid và Spectral Rolloff có thể có giá trị hàng nghìn Hz, trong khi RMS hoặc ZCR thường nằm trong khoảng nhỏ hơn nhiều. Nếu so sánh trực tiếp vector gốc, các thuộc tính có giá trị lớn có thể chi phối kết quả.

Để khắc phục vấn đề này, hệ thống sử dụng hai bước chuẩn hóa:

```text
raw feature vector
→ Z-score normalization theo thống kê của toàn bộ CSDL
→ L2 Normalization
```

### **Bước 1: Z-score normalization**

Với mỗi chiều đặc trưng, hệ thống tính giá trị trung bình và độ lệch chuẩn trên toàn bộ các segment trong cơ sở dữ liệu:

```text
zᵢ = (vᵢ - μᵢ) / σᵢ
```

Trong đó:

- `vᵢ` là giá trị gốc của chiều đặc trưng thứ i.
- `μᵢ` là giá trị trung bình của chiều thứ i trên toàn bộ CSDL.
- `σᵢ` là độ lệch chuẩn của chiều thứ i trên toàn bộ CSDL.
- `zᵢ` là giá trị sau chuẩn hóa Z-score.

Nếu `σᵢ = 0`, hệ thống thay bằng 1 để tránh chia cho 0. Z-score giúp đưa các thuộc tính có thang đo khác nhau về cùng hệ quy chiếu, tránh việc các thuộc tính có giá trị lớn như Spectral Rolloff, Spectral Centroid hoặc Spectral Bandwidth áp đảo các thuộc tính có giá trị nhỏ như RMS, ZCR hoặc Chroma.

### **Bước 2: L2 Normalization**

Sau khi có vector Z-score `z`, hệ thống tiếp tục chuẩn hóa L2:

```text
v_norm = z / ||z||₂
```

Trong đó:

```text
||z||₂ = sqrt(z₁² + z₂² + ... + zₙ²)
```

- `z` là vector đặc trưng sau Z-score.
- `v_norm` là vector cuối cùng dùng để so sánh.
- `||z||₂` là độ dài Euclid của vector Z-score.

Sau khi chuẩn hóa L2, vector có độ dài bằng 1. Khi sử dụng cosine similarity, việc so sánh tập trung vào hướng của vector, tức cấu trúc tương đối giữa các thuộc tính. Kết hợp Z-score và L2 giúp hệ thống vừa cân bằng thang đo giữa các chiều đặc trưng, vừa phù hợp với độ đo cosine similarity.

Các tham số `mean_vector` và `std_vector` được lưu trong bảng `feature_stats`. Khi có file truy vấn mới, hệ thống trích xuất vector 78 chiều, chuẩn hóa Z-score bằng chính thống kê của CSDL, sau đó chuẩn hóa L2 và so sánh với các vector đã lưu.

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

**Ví dụ:** Nếu một file âm thanh sau khi crawl có thời lượng khoảng 30 giây

→ thường được chia thành khoảng 11 đoạn với cửa sổ 5 giây và bước trượt 2,5 giây.

→ lưu tương ứng khoảng 11 vector đặc trưng trong bảng track\_segments. Nếu thời lượng file khác 30 giây, số đoạn sẽ thay đổi theo thời lượng thực tế.

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

### ***3.1.2. Thiết kế bảng track\_segments***

Bảng track\_segments dùng để lưu thông tin từng đoạn âm thanh sau khi file được chia bằng cửa sổ trượt. Mỗi đoạn có thời gian bắt đầu, thời gian kết thúc và vector đặc trưng tương ứng. Do thời lượng file sau khi crawl không cố định tuyệt đối, số segment của mỗi file phụ thuộc vào thời lượng thực tế của file đó. Với các file có thời lượng xấp xỉ 30 giây, số đoạn thường khoảng 11 đoạn; các file dài hơn hoặc ngắn hơn sẽ tạo số đoạn khác tương ứng.

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
| spectral\_contrast\_mean | JSON | Mảng 7 giá trị trung bình Spectral Contrast |
| spectral\_contrast\_std | JSON | Mảng 7 giá trị độ lệch chuẩn Spectral Contrast |
| mfcc\_mean | JSON | Mảng 13 giá trị trung bình MFCC |
| mfcc\_std | JSON | Mảng 13 giá trị độ lệch chuẩn MFCC |
| chroma\_mean | JSON | Mảng 12 giá trị trung bình Chroma |
| chroma\_std | JSON | Mảng 12 giá trị độ lệch chuẩn Chroma |
| feature\_vector | JSON | Vector đặc trưng tổng hợp gốc gồm 78 chiều |
| normalized\_vector | JSON | Vector đặc trưng 78 chiều sau khi chuẩn hóa Z-score và L2 |

	

### ***3.1.3. Thiết kế bảng feature\_stats***

Bảng feature\_stats dùng để lưu thống kê chuẩn hóa của toàn bộ cơ sở dữ liệu. Bảng này cần thiết vì hệ thống sử dụng Z-score normalization trước khi chuẩn hóa L2.

| Tên trường | Kiểu dữ liệu | Ý nghĩa |
| ----- | ----- | ----- |
| stats\_key | TEXT | Khóa định danh loại thống kê, ví dụ `zscore` |
| mean\_vector | JSON | Vector gồm 78 giá trị trung bình của từng chiều đặc trưng |
| std\_vector | JSON | Vector gồm 78 giá trị độ lệch chuẩn của từng chiều đặc trưng |

Trong quá trình build database, hệ thống trích xuất và lưu `feature_vector` gốc của các segment trước. Sau khi có toàn bộ vector gốc, hệ thống tính `mean_vector`, `std_vector`, lưu vào bảng feature\_stats, rồi cập nhật `normalized_vector` cho từng segment.

## **3.2. Cơ chế trích xuất và lưu trữ metadata**

Quy trình trích xuất và lưu trữ siêu dữ liệu được thực hiện như sau:

1. Đọc file âm thanh và chuyển về tín hiệu mono.

2. Chia file thành các đoạn nhỏ bằng cửa sổ trượt 5 giây, bước trượt 2,5 giây.

3. Trích xuất các đặc trưng theo frame trong từng đoạn.

4. Tính mean và std cho các đặc trưng dạng chuỗi frame.

5. Ghép các đặc trưng thành vector tổng hợp 78 chiều.

6. Lưu thông tin file vào bảng tracks.

7. Lưu vector đặc trưng gốc của từng đoạn vào bảng track\_segments.

8. Sau khi có toàn bộ vector gốc, tính mean/std cho từng chiều đặc trưng và lưu vào bảng feature\_stats.

9. Chuẩn hóa từng vector bằng Z-score, sau đó chuẩn hóa L2 và cập nhật vào trường normalized\_vector.

Đầu tiên, hệ thống đọc file âm thanh và chuyển tín hiệu âm thanh thành chuỗi mẫu số. Sau đó, file được chia thành nhiều đoạn ngắn bằng cửa sổ trượt. Hệ thống sử dụng cửa sổ 5 giây và bước trượt 2,5 giây. Số đoạn tạo ra không cố định cho mọi file mà phụ thuộc vào thời lượng thực tế của từng file sau khi crawl/cắt. Các file có thời lượng xấp xỉ 30 giây thường tạo khoảng 11 đoạn âm thanh.

Với mỗi đoạn, hệ thống trích xuất các đặc trưng gồm Tempo, OnsetMean, OnsetStd, OnsetDensity, RMSMean, RMSStd, ZCRMean, ZCRStd, Spectral Centroid mean/std, Spectral Bandwidth mean/std, Spectral Rolloff mean/std, Spectral Contrast mean/std, MFCC mean/std và Chroma mean/std. Các đặc trưng này được ghép lại thành một vector đặc trưng tổng hợp gồm 78 chiều.

Sau khi tạo vector đặc trưng gốc, hệ thống chưa chuẩn hóa ngay từng file riêng lẻ. Thay vào đó, quá trình build database được thực hiện theo hai giai đoạn:

```text
Giai đoạn 1: trích xuất và lưu toàn bộ feature_vector gốc
Giai đoạn 2: tính mean/std toàn CSDL, sau đó cập nhật normalized_vector
```

Cụ thể, với toàn bộ các segment trong cơ sở dữ liệu, hệ thống tính `mean_vector` và `std_vector` gồm 78 chiều. Sau đó, mỗi vector đặc trưng gốc được chuẩn hóa bằng Z-score:

```text
zᵢ = (vᵢ - μᵢ) / σᵢ
```

Tiếp theo, vector sau Z-score được chuẩn hóa L2:

```text
v' = z / ||z||₂
```

Vector `v'` là vector cuối cùng được lưu trong trường `normalized_vector` và dùng để so sánh cosine similarity. Cách làm này đảm bảo mọi segment trong database và cả file truy vấn đều được chuẩn hóa theo cùng thống kê của cơ sở dữ liệu.

Cuối cùng, thông tin chung của file âm thanh được lưu vào bảng tracks, vector đặc trưng gốc được lưu trong `feature_vector`, còn vector sau chuẩn hóa Z-score + L2 được lưu trong `normalized_vector` của bảng track\_segments.

## **3.3. Cơ chế tìm kiếm bản nhạc tương đồng**

Khi người dùng đưa vào một file âm thanh truy vấn, hệ thống thực hiện các bước:

1. Nhận file âm thanh truy vấn

2. Đọc và tiền xử lý file truy vấn

3. Chia file truy vấn thành các đoạn nhỏ bằng cửa sổ trượt

4. Trích xuất vector đặc trưng cho từng đoạn

5. Chuẩn hóa vector đặc trưng của truy vấn bằng Z-score theo `mean_vector`, `std_vector` của CSDL, sau đó chuẩn hóa L2

6. Lấy các vector đặc trưng đã chuẩn hóa trong cơ sở dữ liệu

7. Tính độ tương đồng giữa vector truy vấn và vector trong cơ sở dữ liệu

8. Tổng hợp điểm tương đồng theo từng file nhạc

9. Sắp xếp các file theo điểm tương đồng giảm dần

10. Trả về 5 file âm thanh giống nhất

## **3.4. Phương pháp tính độ tương đồng** 

Để so sánh hai vector đặc trưng, hệ thống sử dụng **Cosine Similarity**. Trước khi so sánh, cả vector truy vấn và vector trong cơ sở dữ liệu đều đã được chuẩn hóa theo cùng quy trình:

```text
feature_vector gốc → Z-score → L2 Normalization
```

Với vector truy vấn là `A` và vector trong cơ sở dữ liệu là `B`, độ tương đồng cosine được tính theo công thức:

```text
cos(A, B) = (A · B) / (||A||₂ × ||B||₂)
```

Trong đó:

- `A · B` là tích vô hướng của hai vector.
- `||A||₂` và `||B||₂` là độ dài Euclid của hai vector.

Do hệ thống đã chuẩn hóa L2 nên `A` và `B` đều là vector đơn vị:

```text
||A||₂ = ||B||₂ = 1
```

Vì vậy, công thức cosine similarity được rút gọn thành:

```text
cos(A, B) = A · B
```

Về mặt lý thuyết, cosine similarity nằm trong khoảng `[-1, 1]`:

- `cos(A, B)` càng gần `1` thì hai đoạn âm thanh càng tương đồng.
- `cos(A, B)` gần `0` nghĩa là hai vector gần như vuông góc, mức tương đồng thấp.
- `cos(A, B)` nhỏ hơn `0` nghĩa là hai vector có hướng đối lập trong không gian đặc trưng.

Trong hệ thống, các kết quả được sắp xếp theo cosine similarity giảm dần. Do đó, bản nhạc có điểm similarity cao hơn được xem là giống với file truy vấn hơn.

# **PHẦN 4\. XÂY DỰNG HỆ THỐNG**

## **4.1. Kiến trúc tổng quát của hệ thống**

Hệ thống được xây dựng theo mô hình web demo cục bộ, gồm hai pha chính:

1. **Pha xây dựng cơ sở dữ liệu**: thu thập file nhạc, trích xuất đặc trưng và lưu vào SQLite.

2. **Pha truy vấn**: nhận file âm thanh đầu vào, trích xuất đặc trưng, so sánh với cơ sở dữ liệu và trả về các bản nhạc tương đồng nhất.

Sơ đồ khối tổng quát của hệ thống có thể mô tả như sau:

```text
Nguồn dữ liệu Pixabay Music
        |
        v
Crawler tải file MP3 và metadata
        |
        v
Thư mục musics/ + file pixabay_music.json
        |
        v
Trích xuất đặc trưng âm thanh theo từng segment
        |
        v
Tính mean/std toàn CSDL → chuẩn hóa Z-score + L2
        |
        v
SQLite Database
(tracks, track_segments, feature_stats)
        |
        v
Flask Web Demo
        |
        v
Upload file truy vấn → trích xuất đặc trưng → so sánh cosine
        |
        v
Top 5 hoặc Top 10 bản nhạc tương đồng nhất
```

Trong kiến trúc này, SQLite đóng vai trò lưu trữ dữ liệu đã xử lý, bao gồm thông tin file nhạc, vector đặc trưng gốc, vector đã chuẩn hóa và thống kê chuẩn hóa. Flask đóng vai trò giao diện web để người dùng upload file truy vấn và xem kết quả tìm kiếm.

## **4.2. Quy trình thực hiện yêu cầu**

Dựa trên yêu cầu của đề bài, hệ thống được thực hiện theo một quy trình hoàn chỉnh từ thu thập dữ liệu, xây dựng cơ sở dữ liệu đặc trưng đến xử lý file truy vấn và trả về kết quả tìm kiếm. Quy trình này có thể mô tả thành các bước sau:

### ***Bước 1: Thu thập dữ liệu nhạc không lời***

Trước hết, hệ thống cần xây dựng bộ dữ liệu âm thanh ban đầu. Dữ liệu được thu thập từ Pixabay Music bằng script crawler. Với mỗi bản nhạc, hệ thống lấy các thông tin cơ bản như tiêu đề bản nhạc, đường dẫn trang nguồn, đường dẫn file MP3 và tải file âm thanh về thư mục `musics/`.

Trong quá trình crawl, hệ thống kiểm tra nội dung tải về để tránh lưu nhầm file không phải âm thanh như ảnh thumbnail hoặc nội dung HTML. Các file có kích thước quá nhỏ hoặc nội dung không hợp lệ sẽ bị bỏ qua. Ngoài ra, crawler sử dụng fuzzy matching để hạn chế tải nhiều bản gần trùng nhau theo tên bài hát.

Các file âm thanh sau khi tải về được xử lý để có thời lượng phù hợp. Hệ thống ưu tiên cắt tại điểm lặng hoặc vùng âm lượng thấp gần mốc 30 giây nhằm tránh làm đoạn nhạc bị ngắt đột ngột. Kết quả của bước này gồm:

- Thư mục `musics/` chứa các file âm thanh đã tải.
- File `pixabay_music.json` chứa metadata của các bản nhạc tải thành công.

### ***Bước 2: Đọc danh sách file âm thanh hợp lệ***

Sau khi đã có dữ liệu, hệ thống đọc metadata từ file `pixabay_music.json`. Với mỗi bản ghi, hệ thống kiểm tra trường `local_file` để xác định file âm thanh có thực sự tồn tại trong thư mục dữ liệu hay không.

Chỉ các file tồn tại và đọc được mới được đưa vào bước xây dựng cơ sở dữ liệu. Việc kiểm tra này giúp tránh lỗi khi trích xuất đặc trưng và đảm bảo database chỉ lưu những bản nhạc hợp lệ.

### ***Bước 3: Chia file âm thanh thành các đoạn nhỏ***

Mỗi file âm thanh hợp lệ được chia thành các đoạn nhỏ bằng cửa sổ trượt. Tham số chia đoạn được sử dụng như sau:

```text
Window = 5 giây
Hop = 2,5 giây
Overlap = 50%
```

Cách chia này giúp hệ thống phân tích nội dung âm thanh ở mức cục bộ thay vì chỉ biểu diễn cả bài nhạc bằng một vector duy nhất. Với file có thời lượng xấp xỉ 30 giây, số segment thường vào khoảng 11 đoạn.

Việc chia segment cũng phù hợp với truy vấn thực tế, vì người dùng có thể upload một đoạn ngắn của bài nhạc chứ không nhất thiết là toàn bộ file.

### ***Bước 4: Trích xuất đặc trưng âm thanh cho từng segment***

Với mỗi segment, hệ thống trích xuất một vector đặc trưng 78 chiều. Vector này mô tả nhiều khía cạnh khác nhau của tín hiệu âm thanh như nhịp điệu, năng lượng, dạng sóng, phổ tần số, âm sắc và hòa âm.

Các nhóm đặc trưng chính gồm:

- **Tempo, Onset**: mô tả nhịp độ và sự xuất hiện của các điểm nhấn trong âm thanh.
- **RMS, ZCR**: mô tả năng lượng và đặc điểm miền thời gian của tín hiệu.
- **Spectral Centroid, Spectral Bandwidth, Spectral Rolloff**: mô tả phân bố năng lượng trong miền tần số.
- **Spectral Contrast**: mô tả độ tương phản giữa các dải tần.
- **MFCC**: mô tả âm sắc của âm thanh.
- **Chroma**: mô tả thông tin cao độ và hòa âm.

Kết quả của bước này là `feature_vector` gốc của từng đoạn âm thanh.

### ***Bước 5: Lưu metadata và vector gốc vào SQLite***

Sau khi trích xuất đặc trưng, hệ thống lưu thông tin vào cơ sở dữ liệu SQLite. Cơ sở dữ liệu gồm ba bảng chính:

- `tracks`: lưu thông tin chung của từng bản nhạc như tiêu đề, đường dẫn nguồn, tên file, đường dẫn file và thời lượng.
- `track_segments`: lưu thông tin từng đoạn âm thanh, thời gian bắt đầu, thời gian kết thúc, các thuộc tính đặc trưng và `feature_vector` gốc.
- `feature_stats`: lưu các thống kê dùng cho chuẩn hóa vector.

Ở bước này, các vector đặc trưng gốc được lưu lại để phục vụ tính toán thống kê chuẩn hóa trên toàn bộ cơ sở dữ liệu.

### ***Bước 6: Tính thống kê chuẩn hóa trên toàn bộ database***

Sau khi đã trích xuất toàn bộ vector của các segment, hệ thống tính thống kê trên toàn bộ tập vector trong cơ sở dữ liệu. Hai vector thống kê được sử dụng là:

```text
mean_vector: vector trung bình 78 chiều
std_vector : vector độ lệch chuẩn 78 chiều
```

Hai vector này được lưu vào bảng `feature_stats`. Đây là thông tin quan trọng để đảm bảo mọi vector trong database và vector của file truy vấn sau này đều được chuẩn hóa theo cùng một hệ quy chiếu.

### ***Bước 7: Chuẩn hóa vector đặc trưng trong database***

Mỗi `feature_vector` gốc trong bảng `track_segments` được chuẩn hóa theo hai bước:

```text
feature_vector → Z-score → L2 Normalization
```

Trong đó, Z-score giúp cân bằng thang đo giữa các chiều đặc trưng, còn L2 Normalization đưa vector về vector đơn vị để phù hợp với cosine similarity.

Kết quả chuẩn hóa cuối cùng được lưu vào trường `normalized_vector` của bảng `track_segments`. Sau bước này, cơ sở dữ liệu đã sẵn sàng để phục vụ tìm kiếm tương đồng.

### ***Bước 8: Người dùng upload file âm thanh truy vấn***

Khi sử dụng hệ thống demo, người dùng truy cập giao diện web Flask và upload một file âm thanh cần tìm kiếm. File truy vấn có thể là một đoạn nhạc đã có trong cơ sở dữ liệu hoặc một file âm thanh chưa có trong dữ liệu.

Hệ thống kiểm tra định dạng file để đảm bảo file thuộc nhóm định dạng được hỗ trợ như `mp3`, `wav`, `m4a`, `ogg`, `flac`, `aac` hoặc `webm`. Sau đó, file được lưu tạm vào thư mục `uploads/` để xử lý.

### ***Bước 9: Trích xuất và chuẩn hóa đặc trưng của file truy vấn***

File truy vấn được xử lý bằng cùng quy trình với dữ liệu trong database. Cụ thể, hệ thống chia file thành segment bằng cửa sổ 5 giây, bước trượt 2,5 giây, sau đó trích xuất vector đặc trưng 78 chiều cho từng segment.

Vector truy vấn không được chuẩn hóa bằng thống kê riêng của file upload. Thay vào đó, hệ thống sử dụng `mean_vector` và `std_vector` đã lưu trong bảng `feature_stats` của cơ sở dữ liệu:

```text
query_feature_vector → Z-score theo mean_vector, std_vector của CSDL → L2 Normalization
```

Cách làm này đảm bảo vector truy vấn và vector trong database nằm trong cùng không gian chuẩn hóa, từ đó có thể so sánh trực tiếp với nhau.

### ***Bước 10: So sánh độ tương đồng bằng Cosine Similarity***

Sau khi chuẩn hóa, hệ thống so sánh từng vector segment của file truy vấn với các `normalized_vector` đã lưu trong SQLite. Độ tương đồng giữa hai segment được tính bằng cosine similarity.

Vì các vector đã được chuẩn hóa L2, cosine similarity phản ánh mức độ gần nhau về hướng giữa hai vector đặc trưng. Giá trị similarity càng cao thì hai đoạn âm thanh càng gần nhau theo bộ thuộc tính đã xây dựng.

### ***Bước 11: Tổng hợp điểm theo từng bản nhạc***

Do một file âm thanh gồm nhiều segment, hệ thống không hiển thị kết quả theo từng segment riêng lẻ. Thay vào đó, kết quả được tổng hợp theo từng bản nhạc để đúng với yêu cầu của đề bài là trả về các file âm thanh giống nhất.

Với mỗi segment của file truy vấn, hệ thống tìm segment khớp tốt nhất trong từng bản nhạc của database. Sau đó, điểm cuối cùng của một bản nhạc được tính bằng trung bình các điểm khớp tốt nhất theo từng segment truy vấn.

Cách tổng hợp này giúp tránh việc một bản nhạc xuất hiện nhiều lần trong danh sách kết quả, đồng thời vẫn tận dụng được thông tin của nhiều đoạn âm thanh trong file truy vấn.

### ***Bước 12: Sắp xếp và hiển thị kết quả***

Sau khi tính điểm similarity cho từng bản nhạc, hệ thống sắp xếp các bản nhạc theo điểm giảm dần và trả về Top 5 hoặc Top 10 kết quả tùy theo lựa chọn của người dùng trên giao diện web.

Mỗi kết quả hiển thị gồm:

- Tên bản nhạc.
- File âm thanh kết quả.
- Điểm tương đồng trung bình.
- Thời lượng file.
- Cặp segment khớp nhất giữa file truy vấn và file trong cơ sở dữ liệu.

Như vậy, quy trình thực hiện yêu cầu của hệ thống bắt đầu từ việc crawl dữ liệu nhạc, xây dựng cơ sở dữ liệu vector đặc trưng, xử lý file truy vấn và cuối cùng trả về danh sách các bản nhạc tương đồng nhất.

## **4.3. Quy trình thực hiện tìm kiếm**

Khi người dùng upload một file âm thanh truy vấn, hệ thống thực hiện quy trình sau:

1. Kiểm tra file upload có tồn tại và thuộc định dạng âm thanh được hỗ trợ.

2. Lưu file truy vấn vào thư mục `uploads/`.

3. Đọc file truy vấn và chia thành các segment bằng cửa sổ 5 giây, bước trượt 2,5 giây.

4. Trích xuất vector đặc trưng 78 chiều cho từng segment truy vấn.

5. Load `mean_vector` và `std_vector` từ bảng `feature_stats`.

6. Chuẩn hóa vector truy vấn bằng Z-score theo thống kê của database.

7. Chuẩn hóa L2 vector sau Z-score.

8. Load toàn bộ `normalized_vector` của các segment trong database.

9. Tính cosine similarity giữa từng segment truy vấn và các segment trong database.

10. Tổng hợp điểm similarity theo từng bản nhạc.

11. Sắp xếp kết quả theo điểm similarity giảm dần.

12. Trả về Top 5 hoặc Top 10 bản nhạc giống nhất theo lựa chọn của người dùng.

## **4.4. Cách tổng hợp điểm theo bản nhạc**

Do mỗi file âm thanh được chia thành nhiều segment, hệ thống không so sánh trực tiếp một file với một file bằng một vector duy nhất. Thay vào đó, việc so sánh được thực hiện ở mức segment.

Với mỗi segment của file truy vấn, hệ thống tìm segment giống nhất trong từng bản nhạc của cơ sở dữ liệu. Sau đó, điểm của một bản nhạc được tính bằng trung bình các điểm khớp tốt nhất theo từng segment truy vấn.

Quy trình tổng hợp điểm như sau:

```text
Với mỗi query_segment:
    Với mỗi track trong database:
        Tìm db_segment của track có similarity cao nhất với query_segment
        Lưu điểm tốt nhất này cho track

Điểm cuối cùng của track = trung bình các điểm tốt nhất theo các query_segment
```

Cách tổng hợp này giúp hệ thống đánh giá mức độ giống nhau giữa file truy vấn và từng bản nhạc dựa trên nhiều đoạn nhỏ, thay vì chỉ dựa vào một cặp segment duy nhất.

Ngoài điểm similarity trung bình, hệ thống cũng lưu lại cặp segment khớp nhất để hiển thị cho người dùng, ví dụ:

```text
Đoạn tải lên thứ 3 (5.00s - 10.00s)
↔ đoạn trong CSDL thứ 4 (7.50s - 12.50s)
```

Thông tin này giúp người dùng hiểu rõ kết quả tìm kiếm được tạo ra từ đoạn nào của file upload và đoạn nào trong file cơ sở dữ liệu.

## **4.5. Kết quả trung gian của quá trình tìm kiếm**

Theo yêu cầu của đề bài, ngoài danh sách Top 5 bản nhạc tương đồng nhất, hệ thống cần trình bày được các kết quả trung gian sinh ra trong quá trình tìm kiếm. Các kết quả trung gian này giúp làm rõ file truy vấn đã được xử lý như thế nào, được chia thành bao nhiêu đoạn, mỗi đoạn có metadata gì, vector đặc trưng được chuẩn hóa ra sao và kết quả so khớp được tổng hợp như thế nào.

Khi một file âm thanh được upload vào hệ thống, quá trình tìm kiếm tạo ra các nhóm kết quả trung gian sau.

### ***4.5.1. Metadata của file truy vấn***

Sau khi người dùng upload file âm thanh, hệ thống lưu file tạm vào thư mục `uploads/` và đọc các thông tin cơ bản của file. Đây là nhóm kết quả trung gian đầu tiên, dùng để xác định file đầu vào trước khi trích xuất đặc trưng.

Các metadata của file truy vấn gồm:

| Thuộc tính | Ý nghĩa |
|---|---|
| `query_name` | Tên file do người dùng upload |
| `query_url` | Đường dẫn tạm để phát lại file truy vấn trên giao diện web |
| `duration` | Thời lượng file truy vấn tính bằng giây |
| `format` | Định dạng file âm thanh, ví dụ `mp3`, `wav`, `m4a` |
| `query_segments` | Số đoạn âm thanh được tách ra từ file truy vấn |

Ví dụ một file truy vấn dài khoảng 30 giây có thể sinh ra khoảng 11 segment khi sử dụng cửa sổ 5 giây và bước trượt 2,5 giây.

### ***4.5.2. Kết quả chia đoạn file truy vấn***

File truy vấn không được so sánh trực tiếp dưới dạng một file duy nhất. Thay vào đó, hệ thống chia file thành nhiều đoạn nhỏ để trích xuất đặc trưng cục bộ. Mỗi đoạn có metadata riêng gồm chỉ số đoạn, thời gian bắt đầu và thời gian kết thúc.

Ví dụ kết quả chia đoạn của một file dài khoảng 30 giây:

| Segment | Start time | End time | Ghi chú |
|---:|---:|---:|---|
| 1 | 0.00s | 5.00s | Đoạn đầu của file truy vấn |
| 2 | 2.50s | 7.50s | Chồng lấn 50% với đoạn 1 |
| 3 | 5.00s | 10.00s | Tiếp tục trượt 2,5 giây |
| ... | ... | ... | ... |
| 11 | 25.00s | 30.00s | Đoạn cuối nếu file dài khoảng 30 giây |

Việc trình bày metadata từng đoạn giúp thấy rõ file truy vấn đã được tách thành các đơn vị nhỏ để so sánh với database. Các trường tương ứng trong chương trình gồm `segment_index`, `start_time` và `end_time`.

### ***4.5.3. Vector đặc trưng của từng đoạn truy vấn***

Sau khi chia đoạn, mỗi segment được trích xuất một vector đặc trưng 78 chiều. Vector này là kết quả trung gian quan trọng nhất vì nó là biểu diễn số của nội dung âm thanh.

Do vector đầy đủ có 78 chiều nên khi trình bày trong báo cáo hoặc giao diện demo, có thể hiển thị một số nhóm đặc trưng tiêu biểu thay vì liệt kê toàn bộ 78 giá trị. Ví dụ:

| Segment | Tempo | RMS mean | ZCR mean | Spectral centroid mean | MFCC mean | Chroma mean |
|---:|---:|---:|---:|---:|---|---|
| 1 | ... | ... | ... | ... | `[m1, m2, ..., m13]` | `[c1, c2, ..., c12]` |
| 2 | ... | ... | ... | ... | `[m1, m2, ..., m13]` | `[c1, c2, ..., c12]` |
| 3 | ... | ... | ... | ... | `[m1, m2, ..., m13]` | `[c1, c2, ..., c12]` |

Trong chương trình, mỗi segment truy vấn có các trường đặc trưng như:

- `tempo`, `onset_mean`, `onset_std`, `onset_density`.
- `rms_mean`, `rms_std`.
- `zcr_mean`, `zcr_std`.
- `spectral_centroid_mean`, `spectral_centroid_std`.
- `spectral_bandwidth_mean`, `spectral_bandwidth_std`.
- `spectral_rolloff_mean`, `spectral_rolloff_std`.
- `spectral_contrast_mean`, `spectral_contrast_std`.
- `mfcc_mean`, `mfcc_std`.
- `chroma_mean`, `chroma_std`.
- `feature_vector` gồm đầy đủ 78 chiều.

Các giá trị này cho biết đặc điểm âm thanh của từng đoạn, ví dụ đoạn nào có năng lượng lớn, đoạn nào có phổ tần số cao, đoạn nào có nhịp rõ hơn hoặc âm sắc khác biệt hơn.

### ***4.5.4. Kết quả chuẩn hóa vector truy vấn***

Sau khi có `feature_vector` gốc, hệ thống chuẩn hóa vector truy vấn bằng thống kê đã lưu trong database. Đây cũng là một kết quả trung gian quan trọng vì nếu không chuẩn hóa cùng hệ quy chiếu, việc so sánh cosine similarity sẽ không ổn định.

Quy trình chuẩn hóa của từng segment truy vấn là:

```text
feature_vector gốc
        ↓
Z-score theo mean_vector và std_vector của database
        ↓
L2 Normalization
        ↓
normalized_vector
```

Các thông tin trung gian có thể trình bày gồm:

| Thuộc tính | Ý nghĩa |
|---|---|
| `feature_dimension` | Số chiều vector, trong hệ thống là 78 |
| `normalization` | Phương pháp chuẩn hóa: Z-score + L2 |
| `mean_vector` | Vector trung bình 78 chiều lấy từ bảng `feature_stats` |
| `std_vector` | Vector độ lệch chuẩn 78 chiều lấy từ bảng `feature_stats` |
| `normalized_vector` | Vector cuối cùng dùng để so sánh cosine similarity |

Trong giao diện hiện tại, hệ thống hiển thị số chiều vector và phương pháp chuẩn hóa. Khi trình bày báo cáo, có thể bổ sung ví dụ một vài chiều đầu của vector trước và sau chuẩn hóa để minh họa.

Ví dụ minh họa:

| Segment | Một vài chiều đầu của `feature_vector` | Một vài chiều đầu của `normalized_vector` |
|---:|---|---|
| 1 | `[tempo, onset_mean, onset_std, ...]` | `[v1, v2, v3, ...]` |
| 2 | `[tempo, onset_mean, onset_std, ...]` | `[v1, v2, v3, ...]` |

### ***4.5.5. Thông tin không gian tìm kiếm trong database***

Trước khi so sánh, hệ thống đọc toàn bộ các segment đã chuẩn hóa trong SQLite. Đây là tập dữ liệu dùng để đối chiếu với file truy vấn.

Các thông tin trung gian của database gồm:

| Thông tin | Ý nghĩa |
|---|---|
| `tracks` | Số bản nhạc trong bảng `tracks` |
| `db_segments` | Số segment trong bảng `track_segments` có `normalized_vector` |
| `feature_dimension` | Số chiều vector đặc trưng |
| `normalization` | Phương pháp chuẩn hóa của vector trong database |

Ví dụ, nếu database có 1000 bản nhạc và mỗi bản nhạc có khoảng 11 segment thì hệ thống sẽ có khoảng 11000 vector segment để so sánh. Khi upload một file truy vấn có 11 segment, hệ thống sẽ lần lượt so sánh từng segment truy vấn với các segment trong database.

### ***4.5.6. Kết quả so khớp segment***

Sau khi có `normalized_vector` của file truy vấn và database, hệ thống tính cosine similarity giữa các segment. Kết quả trung gian ở bước này là các cặp segment có điểm tương đồng cao.

Có thể trình bày kết quả so khớp theo dạng bảng:

| Query segment | DB track | DB segment | Similarity | Nhận xét |
|---:|---|---:|---:|---|
| 1 | Bản nhạc A | 1 | ... | Đoạn khớp tốt nhất của query segment 1 trong bản nhạc A |
| 2 | Bản nhạc A | 2 | ... | Đoạn khớp tốt nhất của query segment 2 trong bản nhạc A |
| 3 | Bản nhạc B | 5 | ... | Đoạn có đặc trưng gần với query segment 3 |

Trong quá trình tính toán, hệ thống không hiển thị tất cả các cặp segment vì số lượng cặp có thể rất lớn. Thay vào đó, hệ thống lưu lại các điểm tốt nhất để tổng hợp theo từng bản nhạc.

### ***4.5.7. Kết quả tổng hợp điểm theo bản nhạc***

Do đề bài yêu cầu trả về các file âm thanh giống nhất, hệ thống tổng hợp điểm từ mức segment lên mức track. Với mỗi bản nhạc, hệ thống lấy các điểm khớp tốt nhất theo từng segment truy vấn rồi tính trung bình.

Bảng trung gian có thể trình bày như sau:

| Track | Điểm tốt nhất với query segment 1 | Điểm tốt nhất với query segment 2 | ... | Điểm trung bình |
|---|---:|---:|---:|---:|
| Bản nhạc A | ... | ... | ... | ... |
| Bản nhạc B | ... | ... | ... | ... |
| Bản nhạc C | ... | ... | ... | ... |

Điểm trung bình này chính là điểm dùng để xếp hạng kết quả. Cách tổng hợp theo track giúp tránh trường hợp cùng một bản nhạc xuất hiện nhiều lần trong Top 5 chỉ vì nhiều segment của nó đều giống file truy vấn.

### ***4.5.8. Kết quả trung gian hiển thị trên giao diện***

Trên trang kết quả của hệ thống demo, các thông tin trung gian được hiển thị gồm:

- Số đoạn được tạo từ file tải lên.
- Số đoạn âm thanh hiện có trong cơ sở dữ liệu.
- Số bản nhạc trong cơ sở dữ liệu.
- Số chiều vector đặc trưng.
- Phương pháp chuẩn hóa đang sử dụng.
- Thời lượng file tải lên.
- Cặp đoạn khớp nhất của từng kết quả.

Ví dụ, nếu file truy vấn dài khoảng 30 giây, hệ thống có thể tạo khoảng 11 segment. Các segment này được chuẩn hóa rồi so sánh với toàn bộ segment đã lưu trong database. Sau đó, hệ thống tổng hợp điểm theo từng bản nhạc và trả về danh sách các bản nhạc có điểm similarity trung bình cao nhất.

Như vậy, kết quả trung gian của quá trình tìm kiếm không chỉ là số lượng segment hay số lượng bản nhạc trong database, mà còn bao gồm metadata của file truy vấn, metadata từng segment, vector đặc trưng, vector chuẩn hóa, các cặp segment khớp tốt và điểm tổng hợp theo từng bản nhạc.

## **4.6. Kết quả tìm kiếm đạt được**

### ***4.6.1. Truy vấn bằng file âm thanh có trong cơ sở dữ liệu***

Khi sử dụng một file âm thanh đã có trong cơ sở dữ liệu làm file truy vấn, hệ thống thường trả về chính bản nhạc đó hoặc các bản rất gần giống ở vị trí cao. Đây là trường hợp kiểm thử cơ bản để xác nhận pipeline trích xuất đặc trưng, chuẩn hóa vector và tính similarity hoạt động đúng.

Trong trường hợp này, điểm similarity của kết quả đúng thường cao vì file truy vấn và file trong database có nhiều segment tương đồng. Nếu file truy vấn là toàn bộ hoặc phần lớn nội dung của bản nhạc đã lưu, các segment truy vấn sẽ có khả năng khớp tốt với các segment tương ứng trong cơ sở dữ liệu.

### ***4.6.2. Truy vấn bằng file âm thanh không có trong cơ sở dữ liệu***

Khi sử dụng một file âm thanh không có sẵn trong cơ sở dữ liệu, hệ thống không thể trả về bản trùng tuyệt đối. Thay vào đó, hệ thống trả về các bản nhạc có nội dung âm thanh gần giống nhất dựa trên vector đặc trưng.

Các kết quả có thể giống file truy vấn ở một số khía cạnh như:

- Nhịp độ tương tự.
- Mức năng lượng gần giống.
- Phối khí hoặc âm sắc tương đồng.
- Phân bố phổ tần số gần nhau.
- Đặc điểm hòa âm/cao độ tương tự.

Trường hợp này thể hiện đúng mục tiêu của hệ thống: không nhận dạng tên bài hát tuyệt đối, mà tìm kiếm các file có nội dung âm thanh tương đồng.

## **4.7. Nhận xét về hệ thống demo**

Hệ thống đã xây dựng được quy trình hoàn chỉnh từ thu thập dữ liệu, trích xuất đặc trưng, lưu trữ trong SQLite đến tìm kiếm và hiển thị kết quả trên giao diện web. Việc chia file thành nhiều segment giúp hệ thống tận dụng được thông tin cục bộ của bản nhạc, phù hợp với truy vấn bằng một đoạn âm thanh ngắn.

Việc sử dụng bộ đặc trưng 78 chiều kết hợp Z-score và L2 Normalization giúp cân bằng thang đo giữa các thuộc tính và phù hợp với cosine similarity. SQLite đáp ứng tốt yêu cầu lưu trữ và demo với quy mô dữ liệu vừa phải. Flask giúp hệ thống có giao diện đơn giản, dễ sử dụng và dễ trình bày khi demo.

Tuy nhiên, do hệ thống không sử dụng chỉ mục vector, quá trình tìm kiếm hiện tại là quét tuần tự toàn bộ các segment trong database. Cách làm này phù hợp với phạm vi bài tập và giúp minh họa rõ cơ chế tìm kiếm, nhưng nếu mở rộng lên dữ liệu rất lớn thì cần xem xét thêm các kỹ thuật tối ưu như chỉ mục vector hoặc approximate nearest neighbor.

# **PHẦN 5. DEMO HỆ THỐNG VÀ ĐÁNH GIÁ KẾT QUẢ**

## **5.1. Mục tiêu demo**

Phần demo nhằm kiểm chứng toàn bộ quy trình của hệ thống tìm kiếm bản nhạc tương đồng bằng âm thanh, từ bước người dùng upload file truy vấn đến bước hệ thống trả về danh sách các bản nhạc giống nhất. Thông qua giao diện web, người dùng có thể quan sát trực tiếp trạng thái cơ sở dữ liệu, gửi file âm thanh đầu vào, xem kết quả tìm kiếm, nghe lại file truy vấn và nghe các file kết quả.

Demo tập trung vào các mục tiêu chính sau:

- Kiểm tra khả năng nhận file âm thanh truy vấn từ người dùng.
- Kiểm tra quá trình trích xuất đặc trưng và chuẩn hóa vector truy vấn.
- Kiểm tra khả năng so sánh file truy vấn với các vector đã lưu trong SQLite.
- Hiển thị Top 5 hoặc Top 10 bản nhạc tương đồng nhất.
- Hiển thị một số thông tin trung gian để giải thích quá trình tìm kiếm.
- Đánh giá mức độ phù hợp của kết quả trả về trong các trường hợp truy vấn khác nhau.

## **5.2. Trang upload file truy vấn**

Trang upload là trang đầu tiên của hệ thống demo. Trang này được xây dựng bằng Flask và có nhiệm vụ cung cấp giao diện để người dùng chọn file âm thanh cần truy vấn. Đây là điểm bắt đầu của quá trình tìm kiếm tương đồng.

Trên trang upload, hệ thống hiển thị tiêu đề của ứng dụng là hệ thống tìm kiếm bản nhạc không lời tương đồng. Bên dưới tiêu đề là mô tả ngắn gọn về cách hệ thống hoạt động: file âm thanh được chia theo cửa sổ 5 giây, trích xuất vector đặc trưng 78 chiều, chuẩn hóa bằng Z-score kết hợp L2 Normalization và so sánh với dữ liệu trong cơ sở dữ liệu.

Trang upload gồm hai nhóm thông tin chính.

### ***5.2.1. Khu vực trạng thái database***

Khu vực trạng thái database cho biết tình trạng dữ liệu hiện có trong hệ thống. Các thông tin được hiển thị gồm:

- **Tracks**: số lượng bản nhạc đã được lưu trong bảng `tracks`.
- **Segments**: số lượng đoạn âm thanh đã được tách và lưu trong bảng `track_segments`.
- **Vector**: số chiều của vector đặc trưng, trong hệ thống này là 78 chiều.
- **Chuẩn hóa**: phương pháp chuẩn hóa vector đang sử dụng, cụ thể là Z-score + L2.

Phần này giúp người dùng biết cơ sở dữ liệu đã được build hay chưa và quy mô dữ liệu hiện tại là bao nhiêu. Nếu số lượng tracks và segments khác 0, hệ thống đã có dữ liệu để thực hiện tìm kiếm.

### ***5.2.2. Khu vực upload file***

Khu vực upload file cho phép người dùng chọn một file âm thanh từ máy tính để làm đầu vào truy vấn. Hệ thống hỗ trợ các định dạng âm thanh phổ biến như `mp3`, `wav`, `m4a`, `ogg`, `flac`, `aac` và `webm`.

Ngoài ô chọn file, trang upload còn có lựa chọn số lượng kết quả cần hiển thị. Người dùng có thể chọn:

- **5 bản ghi**: hiển thị 5 bản nhạc tương đồng nhất.
- **10 bản ghi**: hiển thị 10 bản nhạc tương đồng nhất.

Sau khi chọn file và số lượng kết quả, người dùng nhấn nút **Tìm kiếm**. Khi đó, file được gửi tới route `/search` của Flask. Hệ thống lưu file tạm vào thư mục `uploads/`, sau đó tiến hành trích xuất đặc trưng, chuẩn hóa vector truy vấn và so sánh với các vector đã lưu trong SQLite.

Vai trò của trang upload là tạo giao diện nhập liệu đơn giản, trực quan và dễ sử dụng. Người dùng không cần thao tác trực tiếp với chương trình Python hay cơ sở dữ liệu mà chỉ cần chọn file âm thanh và nhấn nút tìm kiếm.

## **5.3. Trang kết quả tìm kiếm**

Sau khi hệ thống xử lý file truy vấn, người dùng được chuyển sang trang kết quả. Trang này hiển thị file âm thanh đã upload, các thông tin trung gian của quá trình tìm kiếm và danh sách các bản nhạc tương đồng nhất.

### ***5.3.1. Khu vực thông tin file truy vấn***

Ở đầu trang kết quả, hệ thống hiển thị tên file âm thanh mà người dùng đã upload. Bên dưới tên file là trình phát audio để người dùng có thể nghe lại file truy vấn. Việc hiển thị audio đầu vào giúp người dùng dễ so sánh trực tiếp giữa file truy vấn và các file kết quả.

Trang này cũng có liên kết quay lại trang upload để thực hiện một truy vấn khác.

### ***5.3.2. Khu vực kết quả trung gian***

Khu vực kết quả trung gian mô tả một số thông tin sinh ra trong quá trình xử lý truy vấn. Các thông tin này gồm:

- **Số đoạn tải lên**: số segment được tách ra từ file truy vấn.
- **Số đoạn trong CSDL**: tổng số segment đã lưu trong cơ sở dữ liệu và được dùng để so sánh.
- **Số bản nhạc**: số lượng track trong cơ sở dữ liệu.
- **Vector**: số chiều vector và phương pháp chuẩn hóa đang sử dụng.
- **Thời lượng file tải lên**: độ dài thực tế của file truy vấn tính bằng giây.

Các thông tin trung gian này giúp giải thích rõ hơn quá trình tìm kiếm. Ví dụ, nếu file truy vấn dài hơn thì số segment truy vấn có thể nhiều hơn. Số segment trong cơ sở dữ liệu cho biết quy mô không gian tìm kiếm mà hệ thống phải duyệt qua.

### ***5.3.3. Khu vực danh sách kết quả***

Phần danh sách kết quả hiển thị các bản nhạc tương đồng nhất với file truy vấn, được sắp xếp theo điểm tương đồng giảm dần. Mỗi kết quả gồm các thông tin:

- **Thứ hạng kết quả**: ví dụ `#1`, `#2`, `#3`, ...
- **Tên bản nhạc**: lấy từ metadata trong cơ sở dữ liệu.
- **Tên file âm thanh**: tên file được lưu trong thư mục `musics/`.
- **Trình phát audio**: cho phép nghe trực tiếp file kết quả.
- **Độ tương đồng trung bình**: điểm similarity sau khi tổng hợp theo track.
- **Cặp đoạn khớp nhất**: cho biết segment nào của file truy vấn khớp tốt nhất với segment nào trong cơ sở dữ liệu.
- **Thời lượng file**: thời lượng của bản nhạc kết quả.
- **Nguồn Pixabay**: đường dẫn tới trang nguồn nếu metadata có lưu thông tin này.

Điểm tương đồng càng cao thì bản nhạc càng gần với file truy vấn theo bộ đặc trưng âm thanh đã xây dựng. Tuy nhiên, điểm này không phải là xác suất đúng tuyệt đối mà là thước đo mức độ gần nhau trong không gian vector đặc trưng.

Thông tin cặp đoạn khớp nhất giúp người dùng hiểu rõ hơn vì sao một bản nhạc được xếp hạng cao. Nếu một đoạn trong file truy vấn có nhịp điệu, năng lượng, phổ tần số hoặc âm sắc gần với một đoạn trong bản nhạc của cơ sở dữ liệu, điểm similarity giữa hai đoạn đó sẽ cao.

## **5.4. Mẫu đánh giá kết quả demo**

Để đánh giá hệ thống, có thể thực hiện demo với hai nhóm file truy vấn: file đã có trong cơ sở dữ liệu và file chưa có trong cơ sở dữ liệu. Mỗi nhóm kiểm thử phản ánh một khía cạnh khác nhau của bài toán tìm kiếm bản nhạc tương đồng.

### ***5.4.1. Trường hợp 1: Truy vấn bằng file đã có trong cơ sở dữ liệu***

Ở trường hợp này, chọn một file âm thanh trong thư mục `musics/` làm file truy vấn. Vì file này đã tồn tại trong cơ sở dữ liệu, kết quả mong đợi là chính file đó xuất hiện ở vị trí cao nhất hoặc nằm trong nhóm kết quả đầu tiên.

Mẫu ghi nhận kết quả:

| Tiêu chí | Kết quả quan sát |
|---|---|
| File truy vấn | Ví dụ: `0004_Caliente Nights...mp3` |
| File có tồn tại trong CSDL không? | Có |
| Số segment của file truy vấn | Ví dụ: 11 segment |
| Số segment trong CSDL | Ví dụ: khoảng 11000 segment |
| Kết quả đúng có xuất hiện trong Top 5 không? | Có |
| Vị trí của kết quả đúng | Ví dụ: Top 1 |
| Điểm similarity của kết quả đúng | Ví dụ: cao nhất trong danh sách |
| Nhận xét | Hệ thống nhận ra file có nội dung trùng hoặc rất gần với dữ liệu đã lưu. |

Nhận xét mẫu:

Khi sử dụng file đã có trong cơ sở dữ liệu làm truy vấn, hệ thống trả về chính bản nhạc đó ở vị trí cao trong danh sách kết quả. Điều này cho thấy quy trình trích xuất đặc trưng, chuẩn hóa vector và so sánh cosine similarity hoạt động đúng. Các segment của file truy vấn có độ tương đồng cao với các segment tương ứng đã lưu trong cơ sở dữ liệu, do đó điểm similarity trung bình của track này cao hơn các bản nhạc khác.

### ***5.4.2. Trường hợp 2: Truy vấn bằng file chưa có trong cơ sở dữ liệu***

Ở trường hợp này, sử dụng một file âm thanh không nằm trong thư mục dữ liệu ban đầu. Vì file truy vấn chưa có trong cơ sở dữ liệu, hệ thống không thể trả về bản trùng tuyệt đối. Kết quả cần đánh giá theo mức độ giống nhau về nội dung âm thanh như nhịp độ, năng lượng, âm sắc, phổ tần số hoặc hòa âm.

Mẫu ghi nhận kết quả:

| Tiêu chí | Kết quả quan sát |
|---|---|
| File truy vấn | Ví dụ: một file nhạc không lời bên ngoài bộ dữ liệu |
| File có tồn tại trong CSDL không? | Không |
| Số segment của file truy vấn | Ví dụ: 8 segment |
| Số kết quả hiển thị | Top 5 hoặc Top 10 |
| Kết quả có cùng phong cách/nhịp điệu không? | Có/Không, mô tả cụ thể |
| Kết quả có âm sắc hoặc năng lượng gần giống không? | Có/Không, mô tả cụ thể |
| Điểm similarity của Top 1 | Ghi điểm quan sát được |
| Nhận xét | Hệ thống trả về các bản nhạc gần giống về đặc trưng âm thanh, không phải bản trùng tuyệt đối. |

Nhận xét mẫu:

Khi sử dụng file chưa có trong cơ sở dữ liệu, hệ thống vẫn trả về danh sách các bản nhạc có độ tương đồng cao nhất theo vector đặc trưng. Các kết quả đầu thường có một số đặc điểm gần với file truy vấn như nhịp độ tương tự, mức năng lượng gần nhau hoặc màu sắc âm thanh tương đồng. Tuy nhiên, do hệ thống tìm kiếm dựa trên đặc trưng âm thanh tổng quát chứ không nhận dạng giai điệu chính xác tuyệt đối, kết quả có thể chỉ giống ở một số khía cạnh nhất định thay vì giống hoàn toàn về giai điệu.

### ***5.4.3. Bảng đánh giá tổng hợp***

Có thể tổng hợp kết quả demo bằng bảng sau:

| Lần thử | Loại file truy vấn | Số segment truy vấn | Top 1 | Điểm Top 1 | Kết quả mong đợi | Đánh giá |
|---|---|---:|---|---:|---|---|
| 1 | File có trong CSDL | ... | ... | ... | File gốc xuất hiện Top 1/Top 5 | Đạt/Chưa đạt |
| 2 | File có trong CSDL | ... | ... | ... | File gốc xuất hiện Top 1/Top 5 | Đạt/Chưa đạt |
| 3 | File ngoài CSDL | ... | ... | ... | Kết quả có đặc trưng âm thanh gần giống | Đạt/Chưa đạt |
| 4 | File ngoài CSDL | ... | ... | ... | Kết quả có đặc trưng âm thanh gần giống | Đạt/Chưa đạt |

Tiêu chí đánh giá đề xuất:

- Với file đã có trong cơ sở dữ liệu, hệ thống được xem là đạt nếu file gốc xuất hiện trong Top 5, tốt hơn nếu xuất hiện ở Top 1.
- Với file chưa có trong cơ sở dữ liệu, hệ thống được xem là đạt nếu các kết quả đầu có một số đặc trưng âm thanh tương đồng khi nghe lại, chẳng hạn nhịp độ, mức năng lượng, âm sắc hoặc phong cách phối khí.
- Kết quả cần được đánh giá kết hợp giữa điểm similarity và cảm nhận nghe thực tế, vì vector đặc trưng chỉ biểu diễn một phần nội dung âm nhạc.

## **5.5. Nhận xét kết quả đạt được**

Qua quá trình demo, hệ thống đã đáp ứng được yêu cầu cơ bản của đề bài. Hệ thống cho phép người dùng upload một file âm thanh, xử lý file truy vấn, tìm kiếm trong cơ sở dữ liệu SQLite và trả về danh sách các bản nhạc tương đồng nhất. Giao diện web gồm hai trang đơn giản, dễ sử dụng: trang upload file và trang hiển thị kết quả.

Các kết quả trung gian như số segment truy vấn, số segment trong cơ sở dữ liệu, số bản nhạc, số chiều vector và phương pháp chuẩn hóa giúp quá trình demo rõ ràng hơn. Người dùng không chỉ xem được danh sách kết quả cuối cùng mà còn hiểu được hệ thống đã xử lý file âm thanh theo các bước nào.

Đối với truy vấn bằng file đã có trong cơ sở dữ liệu, hệ thống có khả năng trả về file gốc ở thứ hạng cao. Điều này chứng minh rằng cách biểu diễn vector đặc trưng và cơ chế cosine similarity có hiệu quả trong việc nhận ra các file giống nhau. Đối với truy vấn bằng file chưa có trong cơ sở dữ liệu, hệ thống vẫn có thể tìm được các bản nhạc gần giống theo một số đặc điểm âm thanh như nhịp điệu, năng lượng hoặc âm sắc.

Tuy nhiên, hệ thống vẫn còn một số hạn chế. Thứ nhất, việc tìm kiếm được thực hiện bằng cách quét tuần tự toàn bộ segment nên tốc độ sẽ giảm nếu dữ liệu mở rộng lớn hơn nhiều. Thứ hai, bộ đặc trưng thủ công 78 chiều chưa thể biểu diễn đầy đủ toàn bộ cấu trúc giai điệu và cảm xúc của bản nhạc. Thứ ba, kết quả tương đồng đôi khi phụ thuộc vào từng đoạn cụ thể của file truy vấn, nhất là khi file upload có độ dài ngắn hoặc có phần âm thanh không đại diện cho toàn bộ bài.

Nhìn chung, hệ thống đã hoàn thành mục tiêu demo của đề tài: xây dựng được cơ sở dữ liệu âm thanh, trích xuất đặc trưng, tìm kiếm tương đồng bằng vector và hiển thị kết quả trên giao diện web. Đây là nền tảng có thể tiếp tục mở rộng bằng các kỹ thuật tối ưu tìm kiếm vector, bổ sung đặc trưng học sâu hoặc cải thiện cách tổng hợp điểm theo toàn bộ bài nhạc.
