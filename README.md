# カーシェア・高速代 割り勘精算ツール

ChatGPTとGeminiで作成したコードをベースにしているため、予期せぬ不具合があるかもしれません。  
**初心者が作成したコードです。**  
**このコードによる損失に関して作成者は一切の責任を負いません。**

## 概要

これは、旅行などで発生したレンタカー代や高速代などの諸費用を、複数人で割り勘精算するためのコマンドラインツールです。利用日数や区間ごとの利用人数に応じて、公平な割り勘計算を行います。

## 主な機能

  - **複数台の車両費用に対応**: レンタカーを複数台借りた場合の費用入力が可能です。
  - **利用日数に応じた按分**: 車両費用は、各参加者の利用日数（0.5日単位）に応じて按分されます。
  - **高速料金の個別精算**: 高速道路の利用区間ごとに、その区間を利用したメンバーだけで料金を割り勘します。
  - **立替払いに対応**: 誰がいくら支払ったかを記録し、最終的な差額を自動で計算します。
  - **分かりやすい結果表示**: `tabulate`ライブラリを使用し、誰がいくら支払うべきか、または受け取るべきかを表形式で分かりやすく表示します。
  - **LINE送信用メッセージ**: 精算結果をLINEなどで簡単に共有するためのシンプルなメッセージを生成します。
  - **入力チェックと検算機能**: 不正な入力（自然数でない、空欄など）を防ぐ機能と、最終的な請求額と支払額の合計が一致するかを検証する機能を備えています。

## 動作環境

  - Python 3.x

### 必要なライブラリ

このプログラムは`tabulate`ライブラリを使用します。以下のコマンドでインストールしてください。

```bash
pip install tabulate
```

## 使い方

1.  ターミナル（コマンドプロンプト）で以下のコマンドを実行します。
    ```bash
    python [ファイル名].py
    ```
2.  **車の情報入力**: 使用した車の台数を入力し、それぞれの費用と支払者の名前を入力します。
3.  **参加者情報入力**: 車を利用した全員の人数を入力し、それぞれの名前と利用日数を入力します。
4.  **高速料金入力**: 高速道路を利用した場合、`y`を入力して精算に進みます。区間ごとの料金、支払者、その区間の利用人数とメンバーの名前を入力します。
5.  **結果表示**: 全ての入力が終わると、精算結果のテーブルとLINE送信用メッセージが表示されます。

## 計算ロジック

  - **車両費用**: 全員の合計利用日数に対する個人の利用日数の割合に応じて、車両費用の総額を按分します。
      - `個人の負担額 = 車両費用の合計 × (個人の利用日数 / 全員の合計利用日数)`
  - **高速料金**: 各区間の高速料金は、その区間を利用した人数で均等に割り勘されます。
      - `個人の負担額 = 高速料金 / その区間の利用人数`
  - **最終的な差額**: 各自の立替額から、計算された負担額の合計を差し引いて算出します。
      - `差額 = 個人の支払合計額 - (個人の車両費用負担額 + 個人の高速料金負担額)`
