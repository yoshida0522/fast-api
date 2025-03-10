# FastAPI

## 【概要】

このプロジェクトは FastAPI を使用して構築されたバックエンド API です。<br>

## 【環境変数】

以下の環境変数を設定してください。<br>

```bash
MONGO_URI：MongoDB の接続 URI
DIFY_API_KEY：Dify の API キー
```

## 【環境構築】

### 1.必要なパッケージのインストール

```bash
pip install -r requirements.txt
```

### 2.環境変数の設定

.env ファイルを作成し、以下のように記述してください。

```bash
MONGO_URI=your_mongo_uri_here
DIFY_API_KEY=your_dify_api_key_here
```

### 3.サーバーの起動

```bash
uvicorn main:app --reload
```
