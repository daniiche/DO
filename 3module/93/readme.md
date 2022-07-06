Поднял тимсити из файла докер-компоус. Только пришлось прописать каждому контейнеру права рута чтобы можно было писать в директории. 
И Volumes поменял на относительные в папке с компоус файлом (удобнее когда все в одной папке) Еще поменял адрес хоста.
![alt text](https://raw.githubusercontent.com/daniiche/DO/main/3module/93/1.JPG "Logo Title Text 1")

Форкнул репозиторий, создал проект.

Запустил сборку - успешно
![alt text](https://raw.githubusercontent.com/daniiche/DO/main/3module/93/2.JPG "Logo Title Text 1")

Добавил правило, что если происходит изменение в дефолтной ветке (мейн), то запускается один шаг, если по любой другой, то шаг mvn clean test

Для миграции build configuration зашел в  Project Settings | Versioned Settings | Configuration, включил синхронизацию, добавил 
Project settings VCS root


Запушил в мейн - по нему автоматически запустился билд

Создал ветку. добавил класс и его тест
![alt text](https://raw.githubusercontent.com/daniiche/DO/main/3module/93/4.JPG "Logo Title Text 1")

Сделал пуш в новую ветку - билд автоматически не создался. Попробовал несколько раз при разных настройках.

В итоге, Добавил триггер на все ветки и изменил имя в тимсити VCS с admin на свое в гите и автоматическая сборка по пушу в фиче бранч пошла
![alt text](https://github.com/daniiche/DO/blob/main/3module/93/5.JPG "Logo Title Text 1")


Смерджил изменения в ветке в мастер, проверил, что пользовательских артефактов не создалось.

Добавил правило обработки артефактов по расширению файла.
![alt text](https://raw.githubusercontent.com/daniiche/DO/main/3module/93/6.JPG "Logo Title Text 1")

После запуска артефакты сохранились.

Репозиторий.
https://github.com/daniiche/example-teamcity
upd( теперь настройки в репу пушит сам Тимсити https://github.com/daniiche/example-teamcity/tree/master/.teamcity/ExampleTeamcity)
