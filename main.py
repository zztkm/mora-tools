import argparse
import pathlib
import shutil


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
        raise NotADirectoryError(msg)

    # 拡張子の先頭にドットが付いている場合は削除
    extension = extension.lstrip(".")

    # 検索パターンを作成 (例: '*.flac')
    search_pattern = f"*.{extension}"

    # pathlib.Path.rglob() を使用して再帰的にファイルを検索
    # rglob はジェネレータを返すため、list() でリストに変換
    return list(root_path.rglob(search_pattern))


def copy_files_to_directory(
    destination_dir: pathlib.Path,
    source_files: list[pathlib.Path],
) -> None:
    """
    指定されたファイルのリストを、指定されたディレクトリにコピーします。
    コピー先ディレクトリが存在しない場合は作成します。

    Args:
        destination_dir (pathlib.Path): ファイルのコピー先ディレクトリの Path オブジェクト。
        source_files (list[pathlib.Path]): コピーするファイルの Path オブジェクトのリスト。
    """
    if not source_files:
        print("コピー対象のファイルがありません。")
        return

    try:
        # コピー先ディレクトリを作成 (存在しない場合のみ、親ディレクトリも含む)
        destination_dir.mkdir(parents=True, exist_ok=True)
        print(f"コピー先ディレクトリ: {destination_dir}")

        copied_count = 0
        error_count = 0
        for src_path in source_files:
            # コピー先のファイルパスを構築 (ファイル名はそのまま)
            dest_path = destination_dir / src_path.name
            try:
                print(f"コピー中: {src_path} -> {dest_path}")
                # shutil.copy2 を使用してファイルとメタデータをコピー
                shutil.copy2(src_path, dest_path)
                copied_count += 1
            except Exception as e:
                print(f"エラー: {src_path} のコピーに失敗しました - {e}")
                error_count += 1

        print("-" * 20)
        print(f"コピー完了: {copied_count} ファイル成功, {error_count} ファイル失敗")

    except Exception as e:
        print(f"コピー処理中に予期せぬエラーが発生しました: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="指定ディレクトリから特定の拡張子のファイルを検索し、別のディレクトリにコピーします (アーティストとか曲ごとに分かれていて面倒くさいので書いた)",
    )
    parser.add_argument(
        "source_directory",
        type=str,
        help="検索するルートディレクトリのパスを指定します.",
    )
    parser.add_argument(
        "destination_directory",  # コピー先ディレクトリの引数を追加
        type=str,
        help="ファイルをコピーする先のディレクトリパスを指定します.",
    )
    parser.add_argument(
        "-e",
        "--extension",
        type=str,
        default="flac",
        help="検索するファイルの拡張子を指定します (デフォルト: flac).",
    )
    args = parser.parse_args()

    source_root_dir = pathlib.Path(args.source_directory)
    destination_dir = pathlib.Path(
        args.destination_directory,
    )

    try:
        # ファイルを検索
        found_files = find_files_by_extension(source_root_dir, args.extension)

        if found_files:
            print(
                f"{len(found_files)} 個の .{args.extension} ファイルが見つかりました:",
            )
            print("-" * 20)

            # ファイルをコピー
            copy_files_to_directory(destination_dir, found_files)
        else:
            print(
                f"'{source_root_dir}' 以下に .{args.extension} ファイルは見つかりませんでした。",
            )

    except (FileNotFoundError, NotADirectoryError) as e:
        print(f"エラー: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
