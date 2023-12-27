#include "lmshopapp.h"

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
}

std::string LmShopApp::title() const {
    return "LubMi Shop";
}

Wt::Signal<const LmShopApp *, const std::string &> LmShopApp::broadcast_message_;
