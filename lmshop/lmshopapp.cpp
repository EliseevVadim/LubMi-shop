#include "lmshopapp.h"
#include "tools.h"
#include <Wt/WContainerWidget.h>
#include <Wt/WBorderLayout.h>
#include <Wt/WPushButton.h>

LmShopApp::LmShopApp(const Wt::WEnvironment &env, bool embedded):
    EmbeddableApp(env, embedded) {
}

LmShopApp::~LmShopApp() {
    for (auto &conn : connections_) {
        if (conn.isConnected()) {
            conn.disconnect();
        }
    }
}

void LmShopApp::populateInterior() {
    using namespace Wt;
    using namespace std;
    EmbeddableApp::populateInterior();
    auto cw = interior()->addWidget(make_unique<WContainerWidget>(), LayoutPosition::Center);
    auto button = cw->addNew<WPushButton>("XXX");
    button->clicked().connect([this]() {
        doJavaScript("alert(localStorage.boo ? localStorage.boo : 'not set');");
        doJavaScript("localStorage.boo = 777;");
        doJavaScript("Wt.emit(Wt, 'test', localStorage.boo);");
    });
    jsig.connect([](std::string x) {
        std::cout << "It Works: " << x << " " << Tools::gen_uuid() << std::endl;
    });
}

std::string LmShopApp::title() const {
    return "LubMi Shop";
}

Wt::Signal<const LmShopApp *, const std::string &> LmShopApp::broadcast_message_;
