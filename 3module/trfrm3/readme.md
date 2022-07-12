Домашнее задание к занятию "7.3. Основы и принцип работы Терраформ"

Задача 1. Создадим бэкэнд в S3 (необязательно, но крайне желательно).

Если в рамках предыдущего задания у вас уже есть аккаунт AWS, то давайте продолжим знакомство со взаимодействием терраформа и aws.

Создайте s3 бакет, iam роль и пользователя от которого будет работать терраформ. Можно создать отдельного пользователя, а можно использовать созданного в рамках предыдущего задания, просто добавьте ему необходимы права, как описано здесь.
Зарегистрируйте бэкэнд в терраформ проекте как описано по ссылке выше.
Задача 2. Инициализируем проект и создаем воркспейсы.

Выполните terraform init:
если был создан бэкэнд в S3, то терраформ создат файл стейтов в S3 и запись в таблице dynamodb.
иначе будет создан локальный файл со стейтами.
Создайте два воркспейса stage и prod.
В уже созданный aws_instance добавьте зависимость типа инстанса от вокспейса, что бы в разных ворскспейсах использовались разные instance_type.
Добавим count. Для stage должен создаться один экземпляр ec2, а для prod два.
Создайте рядом еще один aws_instance, но теперь определите их количество при помощи for_each, а не count.
Что бы при изменении типа инстанса не возникло ситуации, когда не будет ни одного инстанса добавьте параметр жизненного цикла create_before_destroy = true в один из рессурсов aws_instance.
При желании поэкспериментируйте с другими параметрами и рессурсами.
В виде результата работы пришлите:

Вывод команды terraform workspace list.
Вывод команды terraform plan для воркспейса prod.

## решение

```
DanBookDair:terraform danche$~$ vim ~/.terraformrc

и добавим конфигурацию:

provider_installation {
  network_mirror {
    url = "https://terraform-mirror.yandexcloud.net/"
    include = ["registry.terraform.io/*/*"]
  }
  direct {
    exclude = ["registry.terraform.io/*/*"]
  }
}

terraform init
--сервис акк
yc iam service-account create --name terraform
id: 
folder_id: 

--Назначим роль
yc resource-manager folder add-access-binding ******** --role editor --subject serviceAccount:****************

yc iam access-key create --service-account-name terraform

В provider.tf добавим конфигурацию S3

terraform init

terraform plan

Changes to Outputs:
  + external_ip_address_vm_1 = (known after apply)
  + external_ip_address_vm_2 = (known after apply)
  + internal_ip_address_vm_1 = (known after apply)
  + internal_ip_address_vm_2 = (known after apply)
  + subnet-1                 = (known after apply)
  
--добавим образ
yc compute image list --folder-id standard-images | grep ubuntu-20-04-lts

terraform init
terraform apply

terraform workspace new prod
Created and switched to workspace "prod"!

terraform workspace new stage
Created and switched to workspace "stage"!

--В уже созданный aws_instance добавьте зависимость типа инстанса от воркспейса, чтобы в разных ворскспейсах использовались разные instance_type.
resource "yandex_compute_instance" "vm-1" {
  platform_id = local.yc_instance_type_map[terraform.workspace]
}
  locals {
    yc_instance_type_map = {
      stage = "standard-v1"
      prod  = "standard-v2"
    }
  }
  
--Добавим count. Для stage должен создаться один экземпляр ec2, а для prod два.
resource "yandex_compute_instance" "vm-1" {
  instance_count = local.yc_instance_count[terraform.workspace]
  }
  locals {
      yc_instance_count = {
    stage = 1
    prod = 2
  }
  }
  


```
