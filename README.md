# Robomotion WebPage and API

ロボットモーション記録システム

## Requirements

- Python version
Python 3.6.4 |Anaconda, Inc.|

- Django version
2.0.5

## Usage

### ONLY development environment
`__init__.py`は削除しない
```text
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
```
データベースの削除
```text
rm db.sqlite3
```
マイグレーション
```text
python manage.py makemigrations
python manage.py migrate
```
スーパユーザ作成
```text
python manage.py createsuperuser
```
サーバ起動
```text
python manage.py runserver
```

## システム説明

### ROBOCMS
ロボットの動作保存、バリエーションなどシステムの動作を処理します。
インターフェイスもここで、実装します。

### api_v0
Pepperなど外部から接続する際のapiです。Django REST FRAMEWORKを用いて開発されています。
このapiはベータ版であるため、v0としています。 
