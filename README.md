# Robomotion WebPage and API

ロボットモーション記録システム

## Requirements

- Python version
Python 3.6.4 |Anaconda, Inc.|

- Django version
2.0.5

## システム説明

### ROBOCMS
ロボットの動作保存、バリエーションなどシステムの動作を処理します。
インターフェイスもここで、実装します。

### api_v0
Pepperなど外部から接続する際のapiです。Django REST FRAMEWORKを用いて開発されています。
このapiはベータ版であるため、v0としています。 
