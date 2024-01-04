#include "sh_application.h"
#include "imageprocessor.h"
#include <Wt/WContainerWidget.h>
#include <Wt/WBorderLayout.h>
#include <Wt/WPushButton.h>

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
    auto gl = cw->setLayout(make_unique<WGridLayout>());

    for (int c = 99; c >= 0; c--) {
        auto button = gl->addWidget(make_unique<WPushButton>("Uuid"), c / 4, c % 4, AlignmentFlag::Center);
        button->clicked().connect([this]() {
            doJavaScript(format("alert('{}');", _persist_data.uuid()));
        });
    }
}

std::string ShopApplication::title() const {
    return "LubMi Shop";
}

Wt::Signal<const ShopApplication *, const std::string &> ShopApplication::broadcast_message_;
