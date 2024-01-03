#include "config.h"
#include "ap_application.h"
#include <Wt/Auth/AuthWidget.h>
#include <Wt/WBootstrap2Theme.h>
#include <Wt/WContainerWidget.h>
#include <Wt/Auth/PasswordService.h>

ApApplication::ApApplication(const Wt::WEnvironment &env, bool embedded)
    : EmbeddableApp(env, embedded),
      session_(appRoot() + APANEL_DBASE) {
    session_.login().changed().connect(this, &ApApplication::authEvent);

    root()->addStyleClass("container");
    setTheme(std::make_shared<Wt::WBootstrap2Theme>());
    useStyleSheet("css/style.css");
    
    auto authWidget = std::make_unique<Wt::Auth::AuthWidget>(ApSession::auth(), session_.users(), session_.login());
    authWidget->model()->addPasswordAuth(&ApSession::passwordAuth());
    authWidget->model()->addOAuth(ApSession::oAuth());
    authWidget->setRegistrationEnabled(true);
    authWidget->processEnvironment();
    root()->addWidget(std::move(authWidget));
}

void ApApplication::authEvent() {
    if (session_.login().loggedIn()) {
        const Wt::Auth::User &u = session_.login().user();
        log("notice")
                << "User " << u.id()
                << " (" << u.identity(Wt::Auth::Identity::LoginName) << ")"
                << " logged in.";
    } else {
        log("notice") << "User logged out.";
    }
}
