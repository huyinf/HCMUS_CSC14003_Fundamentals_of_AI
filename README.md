# HCMUS_CSC14003_Fundamentals_of_AI

# BÀI TẬP NHÓM 1

## YÊU CẦU

Thử nghiệm thuật toán tìm kiếm đường đi trên nền game Pac-Man

- Input: bản đồ gồm Pac-man, quá vật, tường, thức ăn biểu diễn bằng các con số được quy định trong file hướng dẫn và lưu ở định dạng file .txt

- Output: Kết quả trò chơi, thời gian, số điểm, đường đi và độ dài đường đi đến đích biểu diễn trực quan bằng thư viện đồ họa (hoặc xuất ra file .txt).

## GIẢI THÍCH

> ### Level 1
> - Chỉ có một đồ ăn.
>
> Trò chơi dừng khi Pac-man tìm được đồ ăn

> ### Level 2
> - Có một đồ ăn và nhiều quái vật cố định.
>
> Trò chơi dừng khi Pac-man tìm được đồ ăn hoặc gặp quái vật.

> ### Level 3
> - Có nhiều đồ ăn và nhiều quái vật di chuyển trong phạm vi giới hạn là 8 ô xung quanh vị trí được khởi tạo.
> - Tầm nhìn của Pac-man là 8 hướng trong phạm vi 3 bước so với vị trí hiện tại.
>
> Trò chơi dừng khi Pac-man ăn hết đồ ăn hoặc gặp quái vật.

> ### Level 4
> - Có nhiều đồ ăn và nhiều quái vật di chuyển tự do
> - Tầm nhìn của Pac-man không hạn chế.
>
> Trò chơi dừng khi Pac-man ăn hết thức ăn hoặc gặp quái vật.

## PHÂN CHIA CÔNG VIỆC

> ### Tạo map tự động
> Input: kích thước
> 
> Ouput: File map.txt theo yêu cầu.
>
> ### Tạo giao diện đồ họa
> Input: map (ma trận)
>
> Output: giao diện, các trạng thái của Pac-man
>
> *Phụ trách*: Đạt + Cường

> ### Cài đặt thuật toán A*
> Input: map (ma trận), điểm bắt đầu (source), điểm đích (destination)
> 
> Output: đường đi (nếu có)
> 
> ### Hàm tính độ dài đường đi
> Input: map, source, destination
> 
> Output: độ dài
>
> *Phụ trách*: Thái Huy + Huy Đức

## Deadline

1. 29/10/2023

## Tools: Github, Python, Overleaf (LaTeX)

