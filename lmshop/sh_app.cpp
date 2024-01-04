#include "sh_app.h"
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
    auto cw = interior()->addWidget(make_unique<WContainerWidget>(), LayoutPosition::Center);

    auto button = cw->addNew<WPushButton>("Uuid");
    button->clicked().connect([this]() {
        doJavaScript(format("alert('{}');", _persist_data.uuid()));
    });

    button = cw->addNew<WPushButton>("Test image processor");
    button->clicked().connect([this]() {
        if (auto image = ImageProcessor::createProductImage("/home/cerberus/30916944.png", true); image) {
            auto i = std::move(*image);
            doJavaScript("alert('Ok');");
        } else {
            doJavaScript(format("alert('{}');", image.error()));
        }

    });
}

std::string ShopApplication::title() const {
    return "LubMi Shop";
}

Wt::Signal<const ShopApplication *, const std::string &> ShopApplication::broadcast_message_;
