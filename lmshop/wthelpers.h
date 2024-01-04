#pragma once
#ifndef ENTRYPOINTMAP_H
#define ENTRYPOINTMAP_H

#include <memory>
#include <Wt/WResource.h>
#include <Wt/WApplication.h>
#include <Wt/WEnvironment.h>
#include <Wt/WServer.h>
#include <Wt/WString.h>

// *INDENT-OFF*
template<class Res> concept WtResource = requires() {
    { std::make_unique<Res>() } -> std::convertible_to<std::unique_ptr<Wt::WResource>>;
};

template<class WidgetSetApp> concept WtEmbeddable = requires(const Wt::WEnvironment &env, bool embedded) {
    { std::make_unique<WidgetSetApp>(env, embedded) }->std::convertible_to<std::unique_ptr<Wt::WApplication>>;
    { std::make_unique<WidgetSetApp>(env, embedded)->populateInterior() };
};
// *INDENT-ON*

/**
 * @brief Makes builder for an App
 */
template <WtEmbeddable App, typename ... T> auto get_builder_for_embeddable(T ... args) {
    using namespace std;
    return [args ...](const Wt::WEnvironment & env) {
        auto app = make_unique<App>(env, args ...);
        app->populateInterior();
        return app;
    };
}

/**
 * @brief Inits server
 * @param argc Parameters count
 * @param argv Parameter strings
 */
template <WtEmbeddable App>
auto init_server(int argc, char *argv[]) {
    using namespace std;
    auto server = make_unique<Wt::WServer>(argv[0]);
    server->setServerConfiguration(argc, argv, WTHTTP_CONFIGURATION);
    server->addEntryPoint(Wt::EntryPointType::Application, get_builder_for_embeddable<App>());
    return server;
}

/**
 * @brief Adds embeddable applications to server
 * @param server -- server to add to
 * @param arg -- relative pathes of embeddables
 */
template <WtEmbeddable ... WE>
void add_embeddables(auto server, auto ... arg) {
    using namespace Wt;
    using namespace std::string_literals;
    ((server->addEntryPoint(EntryPointType::Application, get_builder_for_embeddable<WE>(false), arg),
      server->addEntryPoint(EntryPointType::WidgetSet, get_builder_for_embeddable<WE>(true), arg + ".js"s)), ...);
}

#endif // ENTRYPOINTMAP_H
