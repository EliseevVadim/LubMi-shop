#include "sh_application.h"
#include "imageprocessor.h"
#include <Wt/WContainerWidget.h>
#include <Wt/WBorderLayout.h>
#include <Wt/WHBoxLayout.h>
#include <Wt/WVBoxLayout.h>
#include <Wt/WStackedWidget.h>
#include <Wt/WNavigationBar.h>
#include <Wt/WText.h>
#include <Wt/WMenu.h>
#include <Wt/WImage.h>

ShopApplication::ShopApplication(const Wt::WEnvironment &env, bool embedded):
    EmbeddableApp(env, embedded) {
}

ShopApplication::~ShopApplication() {
    for (auto &conn : connections_) {
        if (conn.isConnected()) {
            conn.disconnect();
        }
    }
}

void ShopApplication::populateInterior() {
    using namespace Wt;
    using namespace std;

    EmbeddableApp::populateInterior();
    auto cw = top()->addWidget(make_unique<WContainerWidget>());
    auto vbl = cw->setLayout(make_unique<WVBoxLayout>());
    // auto stw = make_unique<WStackedWidget>();

    auto header = vbl->addWidget(createHeader());
    // auto main_page = vbl->addWidget(createMainPage());
    // vbl->addWidget(std::move(stw));
    auto footer = vbl->addWidget(createFooter());
}

std::string ShopApplication::title() const {
    return "LubMi Shop";
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createHeader() {
    using namespace std;
    using namespace Wt;

    auto cw = make_unique<WContainerWidget>();
    auto nav = cw->addNew<WNavigationBar>();
    auto stw = cw->addNew<WStackedWidget>();

    auto lmenu = nav->addMenu(make_unique<WMenu>(stw), AlignmentFlag::Right);
    lmenu->addItem("Главная", createMainPage());
    lmenu->addItem("Каталог", createCataloguePage());
    lmenu->addItem("Парфюмерия", createPerfumeryPage());
    lmenu->addItem("Доставка и оплата", createDeliveryPage());
    lmenu->addItem("Уход", createCarePage());
    lmenu->addItem("Контакты", createContactsPage());
    lmenu->addItem("О компании", createAboutCompanyPage());
    lmenu->addStyleClass("me-auto");

    nav->addWidget(make_unique<WImage>(IMAGE_LINK_"logo.svg"))->setMargin(50, Side::Left);
    nav->setWidth(0);
    nav->setResponsive(true);
    nav->setStyleClass("navbar-light bg-light");
    stw->setStyleClass("contents");

    return cw;
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createFooter() {
    using namespace std;
    using namespace Wt;

    auto cw = make_unique<WContainerWidget>();
    auto gl = cw->setLayout(make_unique<WGridLayout>());

    gl->addWidget(make_unique<WText>("ПОКУПАТЕЛЯМ"),            0, 0, AlignmentFlag::Center);
    gl->addWidget(make_unique<WText>("Доставка и оплата"),      1, 0, AlignmentFlag::Left);
    gl->addWidget(make_unique<WText>("Уход"),                   2, 0, AlignmentFlag::Left);
    gl->addWidget(make_unique<WText>("Таблица размеров"),       3, 0, AlignmentFlag::Left);

    gl->addWidget(make_unique<WText>("О КОМПАНИИ"),             0, 1, AlignmentFlag::Center);
    gl->addWidget(make_unique<WText>("О бренде"),               1, 1, AlignmentFlag::Left);
    gl->addWidget(make_unique<WText>("Контакты"),               2, 1, AlignmentFlag::Left);
    gl->addWidget(make_unique<WText>("Отзывы"),                 3, 1, AlignmentFlag::Left);

    gl->addWidget(make_unique<WText>("ПАРТНЕРАМ"),                                   0, 2, AlignmentFlag::Center);
    gl->addWidget(make_unique<WText>("По работе с оптовыми заказами"),               1, 2, AlignmentFlag::Left);
    gl->addWidget(make_unique<WText>("Контакты"),                                    2, 2, AlignmentFlag::Left);
    gl->addWidget(make_unique<WText>("Отзывы"),                                      3, 2, AlignmentFlag::Left);

    gl->addWidget(make_unique<WText>("ПАРТНЕРАМ"),                                   0, 3, AlignmentFlag::Center);
    gl->addWidget(make_unique<WText>("По работе с оптовыми заказами"),               1, 3, AlignmentFlag::Left);
    gl->addWidget(make_unique<WText>("Контакты"),                                    2, 3, AlignmentFlag::Left);
    gl->addWidget(make_unique<WText>("Отзывы"),                                      3, 3, AlignmentFlag::Left);

    cw->setPadding(120, Side::Left | Side::Right);
    cw->decorationStyle().font().setSize(FontSize::Smaller);
    return cw;
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createMainPage() {
    return createUnderConstructionPage("Главная");
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createCataloguePage() {
    return createUnderConstructionPage("Каталог");
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createPerfumeryPage() {
    return createUnderConstructionPage("Парфюмерия");
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createDeliveryPage() {
    return createUnderConstructionPage("Доставка и оплата");
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createCarePage() {
    return createUnderConstructionPage("Уход");
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createContactsPage() {
    return createUnderConstructionPage("Контакты");
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createAboutCompanyPage() {
    return createUnderConstructionPage("О компании");
}

std::unique_ptr<Wt::WContainerWidget> ShopApplication::createUnderConstructionPage(const std::string &page_title) {
    using namespace std;
    using namespace Wt;
    auto cw = make_unique<WContainerWidget>();
    cw->setPadding(10);
    cw->addNew<WText>(format("<h1>{}</h1>", page_title));
    cw->addNew<WText>("Разработка в процессе");
    cw->setHeight(650);
    cw->decorationStyle().setBackgroundColor({"lightgray"});
    return cw;
}

Wt::Signal<const ShopApplication *, const std::string &> ShopApplication::broadcast_message_;
