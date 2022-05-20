```
выполнил действия, контейнер падал. Посмотрел логи, загуглил ошибку - джаве не хватало памяти.
пришлось на впс тариф поднять с бОльшим объемом памяти. Перезапустил виртуалку и конейнер - заработало.

a9ad115a2d4b879ac5b71f1f2427a69e3249e737

поиск установки файла сонар сканнера

создание симлинка
sudo ln -s ./sonar-scanner-4.7.0.2747-linux/bin/sonar-scanner /usr/local/bin/sonar-scanner

изменение прав если файл неисполняемый
sudo chmod +x ./sonar-scanner-4.7.0.2747-linux/bin/sonar-scanner

./sonar-scanner-4.7.0.2747-linux/bin/sonar-scanner \
  -Dsonar.projectKey=test \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://89.108.81.43:9000 \
  -Dsonar.login=a9ad115a2d4b879ac5b71f1f2427a69e3249e737 \
  -Dsonar.coverage.exclusions=fail.py
```
  ссылка на неуспешный прогон
![alt text](https://github.com/daniiche/DO/raw/main/3module/92/scr1.jpg "Logo Title Text 1")

  ссылка на успешный прогон
![alt text](https://github.com/daniiche/DO/raw/main/3module/92/scr2.jpg "Logo Title Text 1")


  файл нексус мавен
https://raw.githubusercontent.com/daniiche/DO/main/3module/92/maven-metadata.xml

файл пом
https://raw.githubusercontent.com/daniiche/DO/main/3module/92/pom.xml

