#include "lmshopapp.h"
#include "wthelpers.h"

#include <format>
#include <memory>
#include <Wt/WServer.h>
#include <Wt/WResource.h>

int main(int argc, char *argv[]) {
    using namespace std;
    using namespace Wt;
    using namespace string_literals;

    try {
        if (auto server = init_server<LmShopApp>(argc, argv); server->start()) {
            add_embeddables<LmShopApp>(server.get(), "/lmshop");
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
