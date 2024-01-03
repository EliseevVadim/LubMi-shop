#pragma once
#ifndef DBODEFS_H
#define DBODEFS_H

#include <Wt/Dbo/Dbo.h>
#include <chrono>

namespace dbo = Wt::Dbo;
template<class T> using dbo_ptr = dbo::ptr<T>;
template<class T> using dbo_ptr_collection = dbo::collection<dbo::ptr<T>>;
namespace Wt::Dbo {
using timestamp = std::chrono::system_clock::time_point;
}

class DbItem {
  public:
    dbo::timestamp created_at {std::chrono::system_clock::now()};    // когда создан
    std::optional<dbo::timestamp> updated_at;                        // когда изменен

  protected:
    template<class Action> void persist(Action &a) {
        dbo::field(a, created_at, "created_at");
        dbo::field(a, updated_at, "updated_at");
    }
};

#endif // DBODEFS_H
