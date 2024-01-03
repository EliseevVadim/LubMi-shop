#pragma once
#ifndef USER_H_
#define USER_H_

#include "dbodefs.h"
#include <Wt/Dbo/Types.h>
#include <Wt/WGlobal.h>

class User;
using AuthInfo = Wt::Auth::Dbo::AuthInfo<User>;

class User: virtual public DbItem {
  public:
    //TODO: additional info

    template<class Action>
    void persist(Action &a) {
        DbItem::persist(a);
    }
};

DBO_EXTERN_TEMPLATES(User)

#endif // USER_H_
