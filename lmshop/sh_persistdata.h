#pragma once
#ifndef PERSISTDATA_H
#define PERSISTDATA_H

#include<string>
#include<unordered_set>
#include<Wt/WGlobal.h>
#include<Wt/WJavaScript.h>
#include<Wt/Json/Object.h>
#include<Wt/WApplication.h>

class PersistData final {
  public:
    PersistData();
    std::string uuid() const noexcept;
    std::string fullName() const noexcept;
    std::string city() const noexcept;
    std::string street() const noexcept;
    std::string building() const noexcept;
    std::string apartment() const noexcept;
    std::string phone() const noexcept;
    std::string email() const noexcept;
    std::unordered_set<std::string> favorites() const noexcept;

    PersistData &update(const std::optional<std::string> &full_name,
                        const std::optional<std::string> &city = {},
                        const std::optional<std::string> &street = {},
                        const std::optional<std::string> &building = {},
                        const std::optional<std::string> &apartment = {},
                        const std::optional<std::string> &phone = {},
                        const std::optional<std::string> &email = {},
                        const std::optional<std::unordered_set<std::string>> &favorites = {});
    PersistData &updateFullName(const std::string &full_name) {
        return update(full_name);
    }
    PersistData &updateCity(const std::string &city) {
        return update({}, city);
    }
    PersistData &updateStreet(const std::string &street) {
        return update({}, {}, street);
    }
    PersistData &updateBuilding(const std::string &building) {
        return update({}, {}, {}, building);
    }
    PersistData &updateApartment(const std::string &apartment) {
        return update({}, {}, {}, {}, apartment);
    }
    PersistData &updatePhone(const std::string &phone) {
        return update({}, {}, {}, {}, {}, phone);
    }
    PersistData &updateEmail(const std::string &email) {
        return update({}, {}, {}, {}, {}, {}, email);
    }
    PersistData &updateFavorites(const std::unordered_set<std::string> &favorites) {
        return update({}, {}, {}, {}, {}, {}, {}, favorites);
    }

  private:
    Wt::Json::Object _json {};
    Wt::JSignal<std::string> _signal_data_exists {Wt::WApplication::instance(), "persist-data-exists"};
    Wt::JSignal<> _signal_data_missed {Wt::WApplication::instance(), "persist-data-missed"};
    void createDefault(bool store = true);
    void store();
};

#endif // PERSISTDATA_H
