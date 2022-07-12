resource "yandex_vpc_network" "network-1" {

  #1 из попыток автоматизировать присвоениe имен:
  name = "vpc-network-${local.yc_instance_count[terraform.workspace]}"

  #Это не работает, так как "The "count" object can only be used in "module", "resource", and "data" blocks, and only when the "count" argument is set"
  /*name = "vpc-network-${count.index}"*/
}

resource "yandex_vpc_subnet" "subnet-1" {
  count          = "${local.yc_instance_count[terraform.workspace] > length(var.yc_region)}"
  /*name           = "yc-auto-subnet-${local.yc_instance_count[terraform.workspace]}"*/
  name           = "yc-auto-subnet-${count.index}"
  /*
  #Оригинальный конфиг:
  name           = "subnet1"*/
  zone           = local.vpc_subnets[terraform.workspace]
  /*
  #Оригинальный конфиг:
  zone           = "ru-central1-a"*/
  network_id     = local.vpc_subnets[terraform.workspace]
  /*network_id     = yandex_vpc_network.network-1.id*/
  v4_cidr_blocks = ["192.168.10.0/24"]
}
