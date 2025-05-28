from pathlib import Path
import pandas as pd


def result_df():
    # カラム
    correct_columns = [
        "年",
        "月",
        "日",
        "回次",
        "場所",
        "日次",
        "レース番号",
        "レース名",
        "クラスコード",
        "芝・ダ",
        "トラックコード",
        "距離",
        "馬場状態",
        "馬名",
        "性別",
        "年齢",
        "騎手名",
        "斤量",
        "頭数",
        "馬番",
        "確定着順",
        "入線着順",
        "異常コード",
        "着差タイム",
        "人気順",
        "走破タイム",
        "走破時計",
        "補正タイム",
        "通過順1",
        "通過順2",
        "通過順3",
        "通過順4",
        "上がり3Fタイム",
        "馬体重",
        "調教師",
        "所属地",
        "賞金",
        "血統登録番号",
        "騎手コード",
        "調教師コード",
        "レースID",
        "馬主名",
        "生産者名",
        "父馬名",
        "母馬名",
        "母の父馬名",
        "毛色",
        "生年月日",
        "単勝オッズ",
        "馬印",
        "レース印",
        "PCI",
    ]
    csv_dir = Path("../csv/")
    csv_files = csv_dir.glob("**/*.CSV")

    # 空のDataFrameを作成
    df = pd.DataFrame()

    # CSVファイルごとに処理
    for file in csv_files:
        # 最適化: chunksizeを指定してメモリ効率良く処理
        chunk_iter = pd.read_csv(
            file, chunksize=10000, encoding="cp932", header=None, names=correct_columns
        )
        for chunk in chunk_iter:
            df = pd.concat([df, chunk], ignore_index=True)
    # git-lfs 対策
    df = df[~df.apply(lambda row: row.astype(str).str.contains("git-lfs", case=False).any(), axis=1)]
    # 扱い易いようにデータの前処理
    # 年、月、日からdateカラム（YYMMDD）を生成
    df["レース日"] = (
        df["年"].astype(str)
        + df["月"].astype(str).str.zfill(2)
        + df["日"].astype(str).str.zfill(2)
    )
    # dateカラムをdatetime型に変換
    df["レース日"] = pd.to_datetime(df["レース日"], format="%y%m%d", yearfirst=True)

    # 生年月日カラムをdatetime型に変換
    df["生年月日"] = pd.to_datetime(df["生年月日"], format="%y%m%d", yearfirst=True)

    # 不要なカラムを削除
    df.drop(columns=["馬印", "レース印"], inplace=True)  # リストで渡す
    return df
