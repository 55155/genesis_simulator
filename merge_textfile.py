import os
import glob

def merge_txt_files(source_dir, output_file):
    """
    source_dir: 텍스트 파일들이 있는 디렉토리 경로 (예: "./output_texts")
    output_file: 병합한 결과를 저장할 파일 이름 (예: "merged_all.txt")
    
    모든 .txt 파일을 찾아, 순서대로 합쳐서 output_file에 저장한다.
    서로 다른 파일 사이에는 '\n' 한 줄(빈 줄)을 추가하여 구분한다.
    """
    # (1) source_dir 경로에서 확장자가 .txt인 파일 목록 수집
    #     sorted()를 통해 알파벳/숫자 순으로 정렬
    txt_files = sorted(glob.glob(os.path.join(source_dir, "*.txt")))
    
    # 만약 txt_files가 비었다면 처리
    if not txt_files:
        print(f"'{source_dir}' 디렉토리에 .txt 파일이 없습니다.")
        return

    # (2) output_file 작성/덮어쓰기 모드("w")로 열기
    with open(output_file, "w", encoding="utf-8") as out_f:
        for i, txt_path in enumerate(txt_files):
            # (3) 각 텍스트 파일을 열어서 읽기
            with open(txt_path, "r", encoding="utf-8") as in_f:
                content = in_f.read()

            # (4) 현재 파일 내용을 out_f에 쓰기
            out_f.write(content)
            
            # (5) 다음 파일과 구분하기 위해 (마지막 파일이 아니라면) '\n' 삽입
            #     혹은 모든 파일 뒤에 공통으로 '\n'을 추가하고 싶다면
            #     파일 읽기 이후 언제나 out_f.write("\n\n") 등으로 해도 됨
            if i < len(txt_files) - 1:
                out_f.write("\n")  # 파일 간 구분을 위한 빈 줄

    print(f"[완료] {len(txt_files)}개의 .txt 파일을 '{output_file}'로 병합했습니다.")


if __name__ == "__main__":
    # 예시 사용
    # 1) 텍스트 파일들이 모여있는 디렉토리
    # source_directory = "/Users/bangseongjin/genesis/api_txt"
    source_directory = "/Users/bangseongjin/genesis/Guide_txt"  
    # 2) 병합 결과를 저장할 파일 이름
    merged_output = "Guide_all.txt"

    merge_txt_files(source_directory, merged_output)
