#include "ap_session.h"
#include "config.h"
#include <Wt/Auth/AuthService.h>
#include <Wt/Auth/HashFunction.h>
#include <Wt/Auth/PasswordService.h>
#include <Wt/Auth/PasswordStrengthValidator.h>
#include <Wt/Auth/PasswordVerifier.h>
#include <Wt/Auth/GoogleService.h>
#include <Wt/Auth/FacebookService.h>
#include <Wt/Auth/Dbo/AuthInfo.h>
#include <Wt/Dbo/backend/Sqlite3.h>

ApSession::ApSession(const std::string &sqlite_db) {
    using namespace Wt;

    auto connection = std::make_unique<Dbo::backend::Sqlite3>(sqlite_db);
    connection->setProperty("show-queries", "true");
    setConnection(std::move(connection));
    mapClass<ApUser>("user");
    mapClass<AuthInfo>("auth_info");
    mapClass<AuthInfo::AuthIdentityType>("auth_identity");
    mapClass<AuthInfo::AuthTokenType>("auth_token");
    users_ = std::make_unique<UserDatabase>(*this);

    try {
        createTables();
        createUser(ADMIN_LOGIN, ADMIN_PASSW, admin);
        std::cerr << "Created database.\n";
    } catch (Wt::Dbo::Exception &e) {
        std::cerr << e.what() << '\n';
        std::cerr << "Using existing database\n";
    }
}

Wt::Auth::AbstractUserDatabase &ApSession::users() {
    return *users_;
}

void ApSession::createUser(const std::string &login, const std::string &password, const Role &role) {
    using namespace Wt;

    dbo::Transaction _(*this);
    auto user = users_->registerNew();
    user.addIdentity(Auth::Identity::LoginName, login);
    passwordAuth().updatePassword(user, password);
    users_->find(user).modify()->setUser(this->add(std::make_unique<ApUser>(role)));
}

std::expected<dbo_ptr<ApUser>, std::string> ApSession::user() const {
    using namespace std;

    if (login_.loggedIn()) {
        return users_->find(login_.user())->user();
    } else {
        return unexpected{"attempt of unauthorized access"};
    }
}

const Wt::Auth::AuthService &ApSession::auth() {
    return auth_service_;
}

const Wt::Auth::PasswordService &ApSession::passwordAuth() {
    return password_service_;
}

std::vector<const Wt::Auth::OAuthService *> ApSession::oAuth() {
    using namespace Wt;

    std::vector<const Auth::OAuthService *> result;
    result.reserve(oauth_services_.size());

    for (const auto &auth : oauth_services_) {
        result.push_back(auth.get());
    }

    return result;
}

void ApSession::configureAuth() {
    using namespace Wt;

    auth_service_.setAuthTokensEnabled(true, "logincookie");
    auth_service_.setEmailVerificationEnabled(false);
    auth_service_.setEmailVerificationRequired(false);

    auto verifier = std::make_unique<Auth::PasswordVerifier>();
    verifier->addHashFunction(std::make_unique<Auth::BCryptHashFunction>(7));

    password_service_.setVerifier(std::move(verifier));
    password_service_.setAttemptThrottlingEnabled(true);
    password_service_.setStrengthValidator(std::make_unique<Auth::PasswordStrengthValidator>());

    if (Auth::GoogleService::configured()) {
        oauth_services_.push_back(std::make_unique<Auth::GoogleService>(auth_service_));
    }

    if (Auth::FacebookService::configured()) {
        oauth_services_.push_back(std::make_unique<Auth::FacebookService>(auth_service_));
    }

    for (const auto &oAuthService : oauth_services_) {
        oAuthService->generateRedirectEndpoint();
    }
}

Wt::Auth::AuthService ApSession::auth_service_;
Wt::Auth::PasswordService ApSession::password_service_(auth_service_);
std::vector<std::unique_ptr<Wt::Auth::OAuthService>> ApSession::oauth_services_;
