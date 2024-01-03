#include "ap_session.h"
#include <Wt/Auth/AuthService.h>
#include <Wt/Auth/HashFunction.h>
#include <Wt/Auth/PasswordService.h>
#include <Wt/Auth/PasswordStrengthValidator.h>
#include <Wt/Auth/PasswordVerifier.h>
#include <Wt/Auth/GoogleService.h>
#include <Wt/Auth/FacebookService.h>
#include <Wt/Auth/Dbo/AuthInfo.h>
#include <Wt/Dbo/backend/Sqlite3.h>

void Session::configureAuth() {
    using namespace Wt;

    myAuthService.setAuthTokensEnabled(true, "logincookie");
    myAuthService.setEmailVerificationEnabled(false);
    myAuthService.setEmailVerificationRequired(false);

    auto verifier = std::make_unique<Auth::PasswordVerifier>();
    verifier->addHashFunction(std::make_unique<Auth::BCryptHashFunction>(7));

    myPasswordService.setVerifier(std::move(verifier));
    myPasswordService.setAttemptThrottlingEnabled(true);
    myPasswordService.setStrengthValidator(std::make_unique<Auth::PasswordStrengthValidator>());

    if (Auth::GoogleService::configured()) {
        myOAuthServices.push_back(std::make_unique<Auth::GoogleService>(myAuthService));
    }

    if (Auth::FacebookService::configured()) {
        myOAuthServices.push_back(std::make_unique<Auth::FacebookService>(myAuthService));
    }

    for (const auto &oAuthService : myOAuthServices) {
        oAuthService->generateRedirectEndpoint();
    }
}

Session::Session(const std::string &sqlite_db) {
    using namespace Wt;

    auto connection = std::make_unique<Dbo::backend::Sqlite3>(sqlite_db);
    connection->setProperty("show-queries", "true");
    setConnection(std::move(connection));
    mapClass<User>("user");
    mapClass<AuthInfo>("auth_info");
    mapClass<AuthInfo::AuthIdentityType>("auth_identity");
    mapClass<AuthInfo::AuthTokenType>("auth_token");

    try {
        createTables();
        std::cerr << "Created database.\n";
    } catch (Wt::Dbo::Exception &e) {
        std::cerr << e.what() << '\n';
        std::cerr << "Using existing database\n";
    }

    users_ = std::make_unique<UserDatabase>(*this);
}

Wt::Auth::AbstractUserDatabase &Session::users() {
    return *users_;
}

dbo::ptr<User> Session::user() const {
    if (login_.loggedIn()) {
        dbo::ptr<AuthInfo> authInfo = users_->find(login_.user());
        return authInfo->user();
    } else {
        return dbo::ptr<User>();
    }
}

const Wt::Auth::AuthService &Session::auth() {
    return myAuthService;
}

const Wt::Auth::PasswordService &Session::passwordAuth() {
    return myPasswordService;
}

std::vector<const Wt::Auth::OAuthService *> Session::oAuth() {
    using namespace Wt;

    std::vector<const Auth::OAuthService *> result;
    result.reserve(myOAuthServices.size());

    for (const auto &auth : myOAuthServices) {
        result.push_back(auth.get());
    }

    return result;
}

Wt::Auth::AuthService Session::myAuthService;
Wt::Auth::PasswordService Session::myPasswordService(Session::myAuthService);
std::vector<std::unique_ptr<Wt::Auth::OAuthService>> Session::myOAuthServices;
