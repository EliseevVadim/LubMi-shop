#include "ap_application.h"
#include "lmshopapp.h"
#include "wthelpers.h"

#include <format>
#include <memory>
#include <Wt/WServer.h>
#include <Wt/WResource.h>
#include <Magick++.h>

int main(int argc, char *argv[]) {
    using namespace std;
    using namespace Wt;
    using namespace string_literals;

    Magick::InitializeMagick(nullptr);

    try {
        if (auto server = init_server<LmShopApp>(argc, argv); server->start()) {
            add_embeddables<LmShopApp, ApApplication>(server.get(), "/lmshop", "/apanel");
            auto signal = WServer::waitForShutdown();
            cerr << format("Shutdown (signal = {})\n", signal);
            server->stop();
        }
    } catch (WServer::Exception &e) {
        cerr << format("Server exception: {}\n", e.what());
    } catch (exception &e) {
        cerr << format("Generic exception: {}\n", e.what());
    } catch (...) { }

    return 0;
}
