from django.shortcuts import render
from django.views import View
from lms.models import Parameter


class PerfumeryView(View):
    @staticmethod
    def get(request, *_, **__):
        return render(request, 'lms/perfumery.html', {
            'page_title': Parameter.value_of("title_perfumery", "Парфюмерия"),
            'page_content': 'perfumery',
            'text_00':
                """#Парфюмерия""",
            'text_01':
                """**Л**юбимые духи — пленительный аромат, изящный флакон, и коробочка с логотипом любимого бренда — объект, пропитанный 
                образами и эмоциями. Чем больше мы знаем об истории духов, о фирме, под чьим именем они выпущены, о личности заказчика 
                или создателя, - тем богаче для нас звучит мелодия аромата.\n\n**К**огда мы душимся, ароматы проникают в нас и постепенно 
                становятся частью нас самих. Если вы любите ароматы и духи для вас не просто парфюмерная композиция, а нечто большее 
                — настроение, воспоминания, эмоции и чувства — то мой парфюмерный магазинчик точно для вас.""",
            'text_02':
                """##В ЧЕМ ОТЛИЧИЯ НИШЕВОЙ, ЛЮКСОВОЙ И МАССМАРКЕТ ПАРФЮМЕРИИ""",
            'text_03':
                """###ВСЮ ПАРФЮМЕРНУЮ ПРОДУКЦИЮ МОЖНО УСЛОВНО ПОДЕЛИТЬ НА 3 «ГРУППЫ»:\n\n- **М**АССМАРКЕТ — массовые продажи, или «товары широкого
                потребления», они не отличаются сложностью ароматов, подбором сырья, тонкостью нот, но у них другое преимущество — 
                доступность. Такие флакончики массово заполоняют полки супермаркетов, павильоны на рынках, в подземных переходах.
                \n\n- **L**UXE - как правило, парфюмерное творчество известных домов мод, ювелиров, парфюмерных компаний. Данная продукция 
                следует тенденциям моды и всегда нравится людям. Такая любовь неслучайна. При создании того, или иного аромата класса люкс, 
                парфюмерные компании инвестируют колоссальные денежные средства на изучение общественного мнения. Парфюмерия Luxe - это 
                всегда грандиозные шоу, широкомасштабные рекламные кампании с участием голливудских звезд, первой величины, топ-моделей 
                и выдающихся спортсменов.\n\n- **Н**ИШЕВАЯ парфюмерия — творение парфюмеров — индивидуалов, или парфюмерных домов с богатой
                историей и огромным опытом в создании парфюма. В таких домах трудятся самые креативные и тонкочувствующие «носы»
                нашего времени. Нишевая парфюмерия (от французского la niche - ниша, ячейка) - не просто запахи, это искусство создания
                аромата, религия парфюмерных нот и философия раскрытия парфюма на коже человека.\n\n**З**ачастую нишевая парфюмерия 
                использует весьма необычное сырьё в производстве своих ароматов. Ароматы могут удивлять, влюблять в себя, смущать, 
                шокировать, погружать в воспоминания; одно точно — они не оставят вас равнодушными. Ноты бывают разными, необычными,
                редко встречающимися. К примеру: Водка и шампанское, гваяковое дерево, белые трюфели и шампиньоны, мокрый табак и 
                древесина на морозе, запах старого авто и медовой патоки.""",
            'text_04':
                """##Твоя выгода!""",
            'text_05':
                """#ВАЖНАЯ ИНФОРМАЦИЯ""",
            'text_06':
                """**И**менно здесь вы можете заказать оригинальную люксовую и нишевую парфюмерию по очень привлекательной стоимости. 
                Так как вы заказываете парфюм напрямую у оптового поставщика, минуя огромную наценку магазинов.""",
            'text_07':
                """**Б**олее того именно у нас вы можете заказать сеты с мини версиями ароматов, чтобы познакомиться и влюбиться в ароматы, 
                которые не пробовали ранее.""",
            'text_08':
                """**И** еще прекрасная новость для тех, кто хочет заниматься парфюмом! У вас есть уникальная возможность заказа парфюма 
                по оптовой стоимости от трёх единиц полноразмерных флаконов.""",
            'text_09':
                """Актуальный каталог и прайс всегда обновляется, поэтому для уточнения по наличию и стоимости, жмите на кнопку 
                «ЗАКАЗАТЬ АРОМАТ».\n\nВас перенаправит в мессенджер для дальнейшей информации. Для начала диалога в мессенджере 
                пишите: «Хочу аромат»""",
            'topics': {
                "Виды парфюмерии":
                    """Любой парфюм состоит из воды, спирта, душистых веществ. В зависимости от их концентрации средство 
                    относят к одному или другому виду парфюмерии. Всего их пять. \n\n###ДУХИ\n\nParfum, Perfume или (в 
                    более редких случаях) Extrait de Parfum — ток обозначают самый концентрированный парфюм, духи. По 
                    стандартам Международной ассоциации по ароматическим веществам (ЕКА) в таком продукте должно быть около
                    20% душистых компонентов, но в некоторых случаях эта цифра может доходить до 40%. У духов самый сильный и
                    стойкий аромат (до 24 часов) — и именно по этой причине они самые дорогие. Духи выпускают в небольших флаконах,
                    но доже 15 мл хватает надолго, ток кок расход самый скромный: для одного применения достаточно одной-двух
                    капель. Кроме того, в духах содержится меньше всего спирта, поэтому они подходят для чувствительной кожи.
                    \n\n###ПАРФЮМЕРНАЯ ВОДА\n\nСамый популярный вид парфюмерии. Доля ароматических веществ в составе парфюмерной воды
                    ниже, чем у духов, - от 15 до 20%. А вот спирта в ней, наоборот, больше. Тем не менее, парфюмерная вода —
                    достаточно насыщенная субстанция, аромат держится от 6 до 8 часов. Её продают во флаконах с пульверизатором,
                    ищите на упаковке надпись Eau de Parfum (EDP)\n\n###ТУАЛЕТНАЯ ВОДА\n\nСодержит от 5 до 15% душистых компонентов,
                    шлейф сохраняется до 4 часов. Парфюм придётся обновлять в течение дня, зато он идеален для офиса и любых других
                    случаев, когда сильное «благоухание» неуместно. Международное обозначение — Eau de Toilette (EDT).
                    \n\n###ОДЕКОЛОН\n\nТрадиционно Eaue de Cologne ассоциируется с мужским парфюмом с высоким содержанием спирта
                    (его в составе действительно много). Концентрация ароматических веществ низкая, от 2 до 5%. Как правило, это
                    облегчённая версия популярных духов или парфюмерной воды. Одеколоны продаются во флаконах большего объёма, так
                    их приходится чаще обновлять в течение дня. Стойкость — около 2-5 часов. Женские ароматы в эту категорию попадают
                    редко.\n\n###АРОМАТИЧЕСКАЯ ВОДА\n\nEau Fraiche с французского переводится как «свежая вода». Но если вы встречаете
                    эту надпись в парфюмерном магазине, за ней скрывается очень лёгкая ароматическая композиция, которая особенно
                    хороша для лета. Это наименее концентрированный из всех типов парфюмов, аромат улетучится в течение часа. Зато
                    и цена самая демократичная. Вариант на случай, когда нужно быстро освежиться — например, в течение дня или
                    перед важной встречей.""",
                "Как воспринимаются ароматы. Ольфакторная пирамида":
                    """Ольфакторная (обонятельная) пирамида — это структура аромата в виде пирамиды нот. Ноты разделены 
                    на три уровня:\n\n- верхние ноты\n\n- средние ноты (или ноты сердца)\n\n- базовые ноты.
                    \n\n###ВЕРХНИЕ НОТЫ.\n\nСоздают первое впечатление аромата. Здесь мы обычно узнаем свежие цветочные, 
                    цитрусовые, и травяные ноты, состоящие из легких молекул, которые быстро испаряются. К ним относятся: 
                    свежесть, зеленые, цитрусовые ноты.\n\n###СРЕДНИЕ НОТЫ.\n\nОбразуют ядро аромата. Они появляются 
                    после того, как рассеиваются верхние ноты, их цель – освежить и смягчить более тяжелый базовый аромат.
                    К ним относятся: цветочные, фруктовые, пряные, древесные ноты. \n\n###БАЗОВЫЕ НОТЫ.\n\nОни раскрываются 
                    последними. Как правило, они состоят из более дерзких ароматов, база добавляет глубину и составляет 
                    ядро аромата. Это конечная нотка часто является якорем запаха, именно её глубокие тона чувствуются в 
                    течение длительного периода, значительно дольше, чем верхние и средние ноты. К ним относятся: мускусные 
                    и амбровые ноты, тяжелые бальзамы, смолы, мхи.""",
                "От чего зависит раскрытие пирамиды нот":
                    """Ароматы, которые наносятся на тело человека, имеют неоднородную структуру. Они состоят из массы 
                    различных параметров, отдельных звуков, раскрытие которых зависит от ряда факторов:
                    \n\n- время года, температура окружающей среды\n\n- естественный запах тела человека, особенности его кожи
                    \n\n- период прошедший после нанесения\n\n- количество ингредиента\n\n- интенсивность потоотделения.
                    \n\nИ каждая мелодия в течение дня стремительно меняет свой ракурс. Какие-то вкусы начинают постепенно 
                    затухать, другие выходят на поверхность и раскрываются с новой силой. Одни слышны где-то на фоне до 
                    самого конца. А часть из них поначалу практически не ощущается, а после нескольких часов становятся все 
                    более явными и отчетливыми.\n\nНа этом принципе, разного действия по времени и интенсивности и создан 
                    механизм градации ингредиентов и их звучания. В полной композиции всегда есть элементы, которые встречают
                    владельца на входе. Они слышны первые несколько минут, игривые и летучие, быстро выветриваются. Вторым 
                    этапом идет основа, которая держится в разных марках от получаса до трех-четырех часов. А в самом фундаменте 
                    всегда располагается база. Это основа и шлейф, которая может остаться с владельцем даже на несколько дней. 
                    Пирамида ароматов в парфюмерии помогает создателю ориентироваться, разделять источники по группам. Включать все 
                    столпы и уровни восприятия. Так он не пропустит ни легких и краткосрочных благоуханий, ни тягучих и основательных.
                    \n\n###ВЕРХНЯЯ НОТА\n\nЭто те оттенки, которые появляются на первых порах. Формируются примерно за пять минут,
                    держатся еще чуть меньше получаса. Стоит сказать, что несмотря на короткий период жизни, интенсивности им 
                    не занимать. Зачастую это свежие и растительные элементы, которые даже в какой-то мере заглушают собой всю 
                    остальную композицию. Благо, они быстро рассеиваются, адаптируется, вплетаются в основу. И становятся единым 
                    целым, продолжением. Но их собственное звучание в этот момент практически полностью затухает. 
                    \n\n####Цитрус\n\nКислинка – это самый необходимый ингредиент, если нужно немного сгладить приторные углы. Чем 
                    выше сладость, тем чаще и сильнее его гасят цитрусом. А кроме того, это очень свежий оттенок, который 
                    позволяет настроить на подвижный и активный лад владельца. Используется часто. В особенности лимон. Но вместе 
                    с ним к группе относятся и мандарин, лайм, и даже имбирь с бергамотом. Стоит сказать, что цитруса всегда 
                    добавляют в меру. Он нужен лишь для гашения основной линии, а сам ей никогда не является. Иначе вкус станет 
                    просто кислым.\n\n####Свежесть\n\nХорошая пирамида парфюма часто использует мяту. Но помимо нее освежающим эффектом
                    обладают водные тона, некоторые овощи, чайные изыски. Опять же, главное назначение заключается в том, чтобы 
                    немного скрывать мощь других ингредиентов. Притуплять их воздействие, иначе они могут подавить всех остальных. 
                    Этакий способ балансировки. Соответственно, применяется он тогда, когда есть элемент, который и стоит немного 
                    затупить.\n\n###СРЕДНЯЯ НОТА\n\nСердце всей композиции. И называется так она неспроста. Это действительно 
                    центральный аромат, который играет на протяжении всего наиболее интенсивного временного отрезка действия.
                    Основа, которая уже обладает и собственным шлейфом. На самом деле, не всегда при выборе духов стоит 
                    ориентироваться именно на сердце. Ведь она раскрывается не для владельца, а как раз для его окружения. Он сам 
                    ощущает ее наименее ярко. Именно тот шлейф, по которому будут судить о человеке другие люди. Поэтому его 
                    мелодия часто подбирается более нейтральная, без агрессии, экзотики. Так, чтобы ее могли нормально воспринять 
                    и оценить подавляющее большинство обывателей. Хотя, бывают и исключения с точностью до наоборот.
                    \n\n####Цветы\n\nСамый частый элемент, который используется для сердца. Хотя, они могут оказаться и в верхней
                    части композиции. В принципе, цветочные ингредиенты очень универсальные. И прекрасно чувствуют себя с 
                    цитрусом, одновременно легко ложатся практически на любую базу. Тем более, их собственная дифференциация 
                    поражает воображение. Они могут быть и томными, и легкими, и глубокими с терпким вкусом, и чуть заметные.
                    \n\n####Пряные\n\n Ольфакторный мир ароматов Востока строится на этих нотах практически полностью. Это яркие
                    специи, перчинка, которая может добавить интригу в любое звучание. А для Европы больше характерны такие 
                    оттенки, как ваниль или кофе.\n\n####Фужерные\n\nХмель, агава, табак и иные наши любимые «зеленые» друзья. 
                    Стоит сказать, что это сердечная нота на любителя. Не все переносят зелень с легкостью. Для многих она 
                    оказывается слишком резкой, несладкой, лишенной изящества. Другие, напротив, считают ее вершиной парфюмерного
                    искусства. Но зеленые звуки всегда индивидуальны и интересны.\n\n####Фруктовые\n\nСобственно, антагонист 
                    прошлого пункта. Фрукты часто отвечают за свежую сладость. Хотя, порой добавляются и кислые, переспелые и 
                    забродившие. Но в большинстве своем, это все же летний, слегка приторный вкус. Подходит, к слову, многим 
                    женщинам вне зависимости от возрастной категории.\n\n###НИЖНЯЯ НОТА\n\nСамый интересный этап – это раскрытие 
                    базы. Фундамент, главная скрипка, ключевой аккорд. Появление томного звучания базовой ноты– это всегда праздник. 
                    Но точно понять, когда она заиграет невозможно.\n\nВ некоторых ароматах она легко вплетается в сердце, и 
                    начало перехода даже невозможно заметить. А в других, момент включения четкий и ясный, меняет всю мелодию.
                    \n\n####Анималистические\n\nПирамида запаха часто обращается к мелодии, которые стараются дотронуться до истинной,
                    живой природы человека. Самый распространенный из ингредиентов, без сомнения, мускус. Второе место заслуженно 
                    можно отдавать коже. Хотя, различных элементов в принципе сотни, если не тысячи.\n\n####Смолы\n\nОчень 
                    долгоиграющие, квинтэссенция природного и навязчивого, томного, глубокого запаха. Используется смола, которая 
                    выделяется зачастую при повреждении или заражении дерева. Поэтому это один из самых дорогих ингредиентов.
                    \n\n####Бальзамические\n\n Пирамида парфюмерной композиции обращается к различным бальзамам. Зачастую либо для
                    собственной изюминки, что бывает в минимуме случаев, либо для подавления другой активной базы. Обычно это 
                    дерево. Если оно слышится грубовато, то бальзамические мелодии становятся сдерживающим фактором.
                    \n\n####Амбровые\n\nОсобый подвид древесных нот, которые отличаются собственным уникальным, томным и несколько 
                    провокационно резким звучанием. Стоит сказать, что выбор на любителя.\n\n####Древесные\n\nНаиболее частая база 
                    в духах унисекс, а также в мужских. Хотя, порой используется и в сугубо женских вкусах. В принципе, дерево 
                    преподносит такую массу оттенков, что в них можно запутаться. Один вид может неповторимо отличаться от другого, 
                    стать полным антиподом, либо полностью копировать.""",
                "Мифы о парфюме":
                    """1. **МИФ**. Во флаконах и тестерах ароматы разного качества.\n\n    Один и тот же аромат экономически не выгодно 
                    производить отдельно для флаконов и тестеров. Все ароматы производятся по одной и той же технологии, поэтому 
                    они абсолютно идентичны в любых флаконах.\n\n1. **МИФ**. Ароматы бывают строго мужские и женские.\n\n    В парфюмерии 
                    нет строгого гендера, и каждый вправе выбрать тот аромат, который нравится. Мужчины и женщины могут пользоваться 
                    любыми ароматами на свой вкус, почти все они - формата унисекс. Истинно мужские и женские ароматы встречаются реже.
                    \n\n1. **МИФ**. Парфюм нужно наносить только на кожу.\n\n    Селективные ароматы раскрываются везде, единственное, 
                    что звучание может быть разным. На коже аромат подстроится под температуру тела и будет звучать в течении дня, 
                    на одежде – может создавать шлейф в течении нескольких дней.\n\n1. **МИФ**. Духи – для особого случая, Туалетная вода
                     – на каждый день.\n\n    Духи и туалетная вода отличаются процентным содержанием масел в составе, это влияет на
                     стойкость, а не повод, куда и когда их надеть. Обращайте внимание, как и сколько парфюма наносите: на каждый 
                     день рекомендуется наносить любой вид парфюмерии облачком, а на выход – на горячие точки, волосы, заднюю часть 
                     шеи.\n\n1. **МИФ**. Синтетические ингредиенты хуже натуральных.\n\n    Сегодня парфюмеры – это химики, которые 
                     создают ароматы в лабораториях. Синтетические компоненты имеют много плюсов: не вызывают аллергию, стоят дешевле 
                     натуральных ингредиентов, ради их добычи не нужно убивать животных.\n\n1. **МИФ**. У настоящей леди должен быть 
                     один парфюм, который будет с ней ассоциироваться.\n\n    Для современной женщины актуально иметь свой «Парфюмерный 
                     гардероб», который включает в себя ароматы на все случаи жизни, чтобы в каждой ситуации аромат был уместен.""",
                "Ошибки в использовании парфюма":
                    """1. Храните ароматы правильно.\n\n    Ароматы очень чувствительны к изменениям окружающей среды, поэтому важно их правильно 
                    хранить. Парфюмы не любят перепадов температур: резкие скачки провоцируют неожиданные химические реакции внутри натуральных 
                    ингредиентов, и как следствие, духи портятся быстрее.\n\n1. Не трите - просто распыляйте.\n\n    Это почти бессознательная 
                    привычка – брызнуть на запястье, а потом растереть. И она плохая. Почему? Трение нагревает кожу и усиливает выработку 
                    определенных ферментов, которые меняют звучание аромата. Больше всего искажаются верхние и средние ноты.\n\n1. Не 
                    оставляйте аромат под прямыми солнечными лучами.\n\n    Ультрафиолетовый свет разрушает формулу запаха и строение 
                    молекул, что ведет к ухудшению звучания и стойкости аромата. И в целом сама композиция аромата нарушается. Лучше всего 
                    хранить в темном месте.""",
                "Как правильно пользоваться парфюмом, для его максимального раскрытия":
                    """- Наносите парфюм на участки тела, которые от природы слегка влажные: верхние ноты аромата будут испаряться не 
                    так быстро. Это, например, внутренняя поверхность локтя, подколенная ямка, зона за ухом.\n\n- Запястья — одна из 
                    точек, где мы можем почувствовать пульс. В таких местах кровеносные сосуды расположены максимально близко к 
                    поверхности тела, а кожа немного теплее. Бушующая кровь слегка «подогревает» аромат, усиливая его звучание. Но не 
                    стоит наносить духи на запястья и тереть их друг о друга. За счет трения звучание аромата будет искажаться. Просто 
                    сбрызните оба запястья.\n\n- Не используйте туалетную или парфюмерную воду на волосах. Формула на спиртовой основе 
                    сушит волосы.\n\n- Аромат плохо «задерживается» на сухой коже, поэтому используйте парфюм сразу после душа или ванны. 
                    Или сначала нанесите лосьон для тела без запаха. Если вы хотите еще больше усилить аромат, сочетайте любимый парфюм 
                    с уходовыми средствами из той же линейки — гелем для душа, мылом, кремом для тела. А чтобы не искажать его звучание, 
                    выбирайте дезодорант без запаха. Или с подобным ароматом — например, туалетную воду Acqua Di Giò используйте в паре с
                    дезодорантом с таким же названием.\n\n- Осторожнее с одеждой! Темное шерстяное пальто переживет пару «пшиков» вашего 
                    любимого парфюма, а вот на шелковом платье могут остаться разводы.\n\n- Если вы любите распылять духи или туалетную 
                    воду в воздухе и затем проходить через ароматное «облако», сначала задержите дыхание и закройте глаза. Важно, чтобы 
                    парфюм не попал на слизистые оболочки носа и глаз.""",
                "Парфюмерные термины":
                    """""",
                "Обозначение символов в парфюмерии":
                    """- (M) man (men), pour homme — Аромат для мужчин\n\n- (W) woman (women), pour femme — Аромат для женщин
                    \n\n- \*\*\* — Аромат перевыпущенный по лицензии\n\n- AF/SH (after shave) — Средство после бритья\n\n- AS/L 
                    (after shave lotion) — Лосьон после бритья\n\n- B/L (body lotion) — Лосьон для тела\n\n- B/spray — Спрей 
                    для тела\n\n- Bath Foam — Пена для ванны\n\n- Bath oil — Масло для ванны и тела\n\n- Beard oil — Масло для бороды
                    \n\n- Body Mist — Дымка для тела\n\n- Candle — Свеча\n\n- DEO — Дезодорант\n\n- Diffusor — Аромат для дома
                    \n\n- EDC (Eau De Cologne) — Одеколон\n\n- EDP — Парфюмированная вода\n\n- EDT (Eau De Toilette) — Туалетная вода
                    \n\n- LIMITED ED. — Лимитированный выпуск\n\n- MINI — Миниатюра, уменьшенная версия парфюма""",
                "10 причин заказать парфюм на распив":
                    """1. Можно приобрести селективный парфюм по приемлемой цене в небольшом объеме. Таким образом, вы сможете избежать 
                    разочарования от покупки сразу большого флакона в том случае, если аромат по каким-то причинам вам не подойдет.
                    \n\n1. Флакон легко умещается в сумке или кармане, что очень удобно и позволяет без труда носить его с собой и брать 
                    в поездки.\n\n1. Большие объемы ароматов имеют свойство надоедать, а маленькие -нет. Обычно миниатюры заканчиваются 
                    быстрее, чем успеют вам разонравиться.\n\n1. Можно взять сразу несколько ароматов разного звучания и менять их по 
                    настроению.\n\n1. Миниатюры смотрятся стильно и эстетично.\n\n1. На сегодняшний день это один из самых модных 
                    подарков – сет из ароматов. У обладателя появится возможность знакомства с дорогими ароматами, не продающимися во многих
                    парфюмерных магазинах.\n\n1. С каждым заказом можно всё лучше разбираться в композициях, начинать понимать, какие
                    ноты и бренды вам больше всего подходят.\n\n1. Можно удивлять окружающих ольфакторными пирамидами.\n\n1. Возможность 
                    продемонстрировать свой изысканный вкус.\n\n1. Покупка сетов из 3-х, 5-ти ароматов всегда идет по более выгодной цене.""",
                "Популярные ароматы.":
                    """1. PINK MOLECULE 090.09\n\n1. ATTAR COLLECTION MUSK KASHMIR\n\n1. JULIETTE HAS A GUN VANILLA VIBES\n\n1. JUICY 
                    COUTURE VIVA LA JUICY\n\n1. MOLECULES ESCENTRIC 02\n\n1. JULIETTE HAS A GUN PEAR INC\n\n1. ZARKOPERFUME THE MUSE
                    \n\n1. ATTAR COLLECTION AZORA\n\n1. TIZIANA TERENZI KIRKE\n\n1. VERTUS NARCOS’IS\n\n1. MONTALE PRETTY FRUITY\n\n1. ATTAR 
                    COLLECTION CRYSTAL LOVE\n\n1. MANCERA SICILY\n\n1. ATTAR COLLECTION THE QUEEN OF SHEBA\n\n1. TIZIANA TERENZI ANDROMEDA
                    \n\n1. EX NIHILO FLEUR NARCOTIQUE\n\n1. BYREDO PARFUMS BLANCHE\n\n1. BYREDO PARFUMS BAL D'AFRIQUE\n\n1. BYREDO GYPSY 
                    WATER\n\n1. MAISON FRANCIS KURKDJIAN BACCARAT ROUGE 540\n\n1. EX NIHILO LUST IN PARADISE\n\n1. KILIAN GOOD GIRL GONE BAD
                    \n\n1. FRANCK BOCLET COCAINE\n\n1. MARC-ANTOINE BARROIS GANYMEDE\n\n1. TOM FORD LOST CHERRY\n\n1. TOM FORD TOBACCO VANILLE
                    \n\n1. JULIETTE HAS A GUN NOT A PERFUME\n\n1. MONTALE INTENSE TIARE\n\n1. BYREDO PARFUMS MOJAVE GHOST""",
            },
        })
