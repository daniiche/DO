
Домашнее задание к занятию "7.2. Облачные провайдеры и синтаксис Terraform."

Зачастую разбираться в новых инструментах гораздо интересней понимая то, как они работают изнутри. Поэтому в рамках первого необязательного задания предлагается завести свою учетную запись в AWS (Amazon Web Services) или Yandex.Cloud. Идеально будет познакомится с обоими облаками, потому что они отличаются.

Задача 1 (вариант с AWS). Регистрация в aws и знакомство с основами (необязательно, но крайне желательно).

Остальные задания можно будет выполнять и без этого аккаунта, но с ним можно будет увидеть полный цикл процессов.

AWS предоставляет достаточно много бесплатных ресурсов в первый год после регистрации, подробно описано здесь.

Создайте аккаут aws.
Установите c aws-cli https://aws.amazon.com/cli/.
Выполните первичную настройку aws-sli https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html.
Создайте IAM политику для терраформа c правами
AmazonEC2FullAccess
AmazonS3FullAccess
AmazonDynamoDBFullAccess
AmazonRDSFullAccess
CloudWatchFullAccess
IAMFullAccess
Добавьте переменные окружения
export AWS_ACCESS_KEY_ID=(your access key id)
export AWS_SECRET_ACCESS_KEY=(your secret access key)
Создайте, остановите и удалите ec2 инстанс (любой с пометкой free tier) через веб интерфейс.
В виде результата задания приложите вывод команды aws configure list.

Задача 1 (Вариант с Yandex.Cloud). Регистрация в ЯО и знакомство с основами (необязательно, но крайне желательно).

Подробная инструкция на русском языке содержится здесь.
Обратите внимание на период бесплатного использования после регистрации аккаунта.
Используйте раздел "Подготовьте облако к работе" для регистрации аккаунта. Далее раздел "Настройте провайдер" для подготовки базового терраформ конфига.
Воспользуйтесь инструкцией на сайте терраформа, что бы не указывать авторизационный токен в коде, а терраформ провайдер брал его из переменных окружений.
Задача 2. Создание aws ec2 или yandex_compute_instance через терраформ.

В каталоге terraform вашего основного репозитория, который был создан в начале курсе, создайте файл main.tf и versions.tf.
Зарегистрируйте провайдер
для aws. В файл main.tf добавьте блок provider, а в versions.tf блок terraform с вложенным блоком required_providers. Укажите любой выбранный вами регион внутри блока provider.
либо для yandex.cloud. Подробную инструкцию можно найти здесь.
Внимание! В гит репозиторий нельзя пушить ваши личные ключи доступа к аккаунту. Поэтому в предыдущем задании мы указывали их в виде переменных окружения.
В файле main.tf воспользуйтесь блоком data "aws_ami для поиска ami образа последнего Ubuntu.
В файле main.tf создайте рессурс
либо ec2 instance. Постарайтесь указать как можно больше параметров для его определения. Минимальный набор параметров указан в первом блоке Example Usage, но желательно, указать большее количество параметров.
либо yandex_compute_image.
Также в случае использования aws:
Добавьте data-блоки aws_caller_identity и aws_region.
В файл outputs.tf поместить блоки output с данными об используемых в данный момент:
AWS account ID,
AWS user ID,
AWS регион, который используется в данный момент,
Приватный IP ec2 инстансы,
Идентификатор подсети в которой создан инстанс.
Если вы выполнили первый пункт, то добейтесь того, что бы команда terraform plan выполнялась без ошибок.
В качестве результата задания предоставьте:

Ответ на вопрос: при помощи какого инструмента (из разобранных на прошлом занятии) можно создать свой образ ami?
Ссылку на репозиторий с исходной конфигурацией терраформа.

```
curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash
ус init
yc iam create-token
MY_Token
export YC_TOKEN=MY_Token

(via VPN)
brew tap hashicorp/tap
brew install hashicorp/tap/terraform

DanBookDair:trfrm2 danche$ mkdir terraform
DanBookDair:trfrm2 danche$ cd terraform/
DanBookDair:terraform danche$ touch main.tf && touch versions.tf
--выберем образ подходящий
yc compute image list --folder-id standard-images | grep "ubuntu-2004-lts "
наполним файлы

terraform init выдает ошибку
│ Could not retrieve the list of available versions for provider yandex-cloud/yandex: could not connect to registry.terraform.io: Failed to request discovery document: 403 Forbidden

VPN
ssh-keygen -t rsa
terraform init
export yandex_cloud_id={my_cloud_id}
export yandex_folder_id={my_yandex_folder_id}
terraform validate
terraform plan

  # yandex_vpc_subnet.subnet-1 will be created
  + resource "yandex_vpc_subnet" "subnet-1" {
      + created_at     = (known after apply)
      + folder_id      = (known after apply)
      + id             = (known after apply)
      + labels         = (known after apply)
      + name           = "subnet1"
      + network_id     = (known after apply)
      + v4_cidr_blocks = [
          + "192.168.10.0/24",
        ]
      + v6_cidr_blocks = (known after apply)
      + zone           = "ru-central1-b"
    }

Plan: 3 to add, 0 to change, 0 to destroy.

Changes to Outputs:
  + external_ip_address_vm_1 = (known after apply)
  + internal_ip_address_vm_1 = (known after apply)

terraform apply
terraform destroy
```
