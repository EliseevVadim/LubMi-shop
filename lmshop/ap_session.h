#pragma once
#ifndef SESSION_H_
#define SESSION_H_

#include "ap_user.h"
#include <Wt/Auth/Login.h>
#include <Wt/Auth/Dbo/UserDatabase.h>
#include <Wt/Dbo/Session.h>
#include <Wt/Dbo/ptr.h>

namespace dbo = Wt::Dbo;
using UserDatabase = Wt::Auth::Dbo::UserDatabase<AuthInfo>;

class Session : public dbo::Session {
  public:
    explicit Session(const std::string &sqlite_db);
    static void configureAuth();
    dbo::ptr<User> user() const;
    Wt::Auth::AbstractUserDatabase &users();
    Wt::Auth::Login &login() {
        return login_;
    }

    static const Wt::Auth::AuthService &auth();
    static const Wt::Auth::PasswordService &passwordAuth();
    static std::vector<const Wt::Auth::OAuthService *> oAuth();

  private:
    std::unique_ptr<UserDatabase> users_;
    Wt::Auth::Login login_;
    static Wt::Auth::AuthService myAuthService;
    static Wt::Auth::PasswordService myPasswordService;
    static std::vector<std::unique_ptr<Wt::Auth::OAuthService>> myOAuthServices;
};

#endif // SESSION_H_
