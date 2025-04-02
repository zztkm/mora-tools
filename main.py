import argparse
import pathlib


def find_files_by_extension(
    root_path: pathlib.Path,
    extension: str = "flac",
) -> list[pathlib.Path]:
    """指定されたルートパス以下のディレクトリを再帰的に検索し、
    指定された拡張子を持つファイルのパスリストを返します.
    """
    # ルートパスの存在とディレクトリであるかを確認
    if not root_path.exists():
        msg = f"指定されたパスが見つかりません: {root_path}"
        raise FileNotFoundError(msg)
    if not root_path.is_dir():
        msg = f"指定されたパスはディレクトリではありません: {root_path}"
        raise NotADirectoryError(
            msg,
        )

    # 拡張子の先頭にドットが付いている場合は削除
    extension = extension.lstrip(".")

    # 検索パターンを作成 (例: '*.flac')
    search_pattern = f"*.{extension}"

    # pathlib.Path.rglob() を使用して再帰的にファイルを検索
    # rglob はジェネレータを返すため、list() でリストに変換
    return list(root_path.rglob(search_pattern))


# --- 関数の使用例 ---

# 検索したいルートディレクトリのパスを pathlib.Path オブジェクトとして指定
# 例: Windows -> pathlib.Path(r"C:\Users\YourUser\Music")
# 例: macOS/Linux -> pathlib.Path("/Users/youruser/Music")
# 今回の例示構造に基づいて C ドライブ直下を仮定


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "directory",
        type=str,
        help="検索するルートディレクトリのパスを指定します.",
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        default="flac",
        help="検索するファイルの拡張子を指定します (デフォルト: flac).",
    )
    args = parser.parse_args()

    target_root_directory = pathlib.Path(args.directory)

    # .flac ファイルを検索 (デフォルト)
    # 必ず pathlib.Path オブジェクトを渡す
    flac_files = find_files_by_extension(target_root_directory, args.extension)
    if flac_files:
        print(".flac ファイルが見つかりました:")
        for file_path in flac_files:
            print(file_path)
    else:
        print(
            f"'{target_root_directory}' 以下に .flac ファイルは見つかりませんでした。",
        )

    print("-" * 20)


if __name__ == "__main__":
    main()
