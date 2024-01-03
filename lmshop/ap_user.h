#pragma once
#ifndef USER_H_
#define USER_H_

#include "dbodefs.h"
#include <bitset>
#include <Wt/Dbo/Types.h>
#include <Wt/WGlobal.h>

class User;
using AuthInfo = Wt::Auth::Dbo::AuthInfo<User>;

using Role = std::bitset<8>;
const Role manager      {0b00000001};
const Role publisher    {0b00000010};
const Role admin        {manager | publisher};

class User: virtual public DbItem {
  public:
    int role;

    void setRole(const Role &r) {
        role = static_cast<decltype(role)>(r.to_ulong());
    }

    Role getRole() {
        return Role(role);
    }

    template<class Action>
    void persist(Action &a) {
        dbo::field(a, role, "role");
        DbItem::persist(a);
    }
};

DBO_EXTERN_TEMPLATES(User)

#endif // USER_H_
