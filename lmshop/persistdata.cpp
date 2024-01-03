#include "persistdata.h"
#include "tools.h"
#include <format>
#include <memory>

#include <Wt/Json/Array.h>
#include <Wt/Json/Serializer.h>
#include <Wt/Json/Parser.h>

#define UUID        "uuid"
#define FULL_NAME   "full_name"
#define CITY        "city"
#define STREET      "street"
#define BUILDING    "building"
#define APARTMENT   "apartment"
#define PHONE       "phone"
#define EMAIL       "email"
#define FAVORITES   "favorites"
#define PSDATANAME  "lmshop_persist_data"

PersistData::PersistData() { //TODO store encrypted on user-side
    using namespace std;
    using namespace Wt;

    shared_ptr<Signals::connection> conn_exists, conn_missed;

    auto disconnect = [conn_exists, conn_missed] () mutable {
        if (conn_exists && conn_exists->isConnected()) {
            conn_exists->disconnect();
        }

        if (conn_missed && conn_missed->isConnected()) {
            conn_missed->disconnect();
        }

        conn_exists.reset();
        conn_missed.reset();
    };

    conn_exists = make_shared<Signals::connection>(_signal_data_exists.connect([this, disconnect](const string & str) mutable {
        disconnect();

        try {
            Json::parse(str, _json);
        } catch (const Json::ParseError &) {
            createDefault();
            return;
        } catch (const Json::TypeException &) {
            createDefault();
            return;
        }

        static const auto keys = {UUID, FULL_NAME, CITY, STREET, BUILDING, APARTMENT, PHONE, EMAIL, FAVORITES};

        for (auto &key : keys) {
            if (!_json.contains(key)) {
                createDefault();
                break;
            }
        }
    }));

    conn_missed = make_shared<Signals::connection>(_signal_data_missed.connect([this, disconnect]() mutable {
        disconnect();
        createDefault();
    }));

    auto jscript = format(R"(if(localStorage.)" PSDATANAME R"() {{{}}} else {{{}}})",
                          _signal_data_exists.createCall({"localStorage." PSDATANAME }),
                          _signal_data_missed.createCall({}));
    WApplication::instance()->doJavaScript(jscript);
}

std::string PersistData::uuid() const noexcept {
    return _json.get(UUID);
}

std::string PersistData::fullName() const noexcept {
    return _json.get(FULL_NAME);
}

std::string PersistData::city() const noexcept {
    return _json.get(CITY);
}

std::string PersistData::street() const noexcept {
    return _json.get(STREET);
}

std::string PersistData::building() const noexcept {
    return _json.get(BUILDING);
}

std::string PersistData::apartment() const noexcept {
    return _json.get(APARTMENT);
}

std::string PersistData::phone() const noexcept {
    return _json.get(PHONE);
}

std::string PersistData::email() const noexcept {
    return _json.get(EMAIL);
}

std::unordered_set<std::string> PersistData::favorites() const noexcept {
    using namespace Wt;
    Json::Array array = _json.get(FAVORITES);
    return {array.begin(), array.end()};
}

PersistData &PersistData::update(const std::optional<std::string> &full_name,
                                 const std::optional<std::string> &city,
                                 const std::optional<std::string> &street,
                                 const std::optional<std::string> &building,
                                 const std::optional<std::string> &apartment,
                                 const std::optional<std::string> &phone,
                                 const std::optional<std::string> &email,
                                 const std::optional<std::unordered_set<std::string>> &favorites) {
    using namespace std;
    using namespace Wt;

    bool need_save = false;

    if (full_name) {
        _json[FULL_NAME] = WString(*full_name);
        need_save = true;
    }

    if (city) {
        _json[CITY] = WString(*city);
        need_save = true;
    }

    if (street) {
        _json[STREET] = WString(*street);
        need_save = true;
    }

    if (building) {
        _json[BUILDING] = WString(*building);
        need_save = true;
    }

    if (apartment) {
        _json[APARTMENT] = WString(*apartment);
        need_save = true;
    }

    if (phone) {
        _json[PHONE] = WString(*phone);
        need_save = true;
    }

    if (email) {
        _json[EMAIL] = WString(*email);
        need_save = true;
    }

    if (favorites) {
        Json::Array array;

        for (const auto &str : *favorites) {
            array.emplace_back(str);
        }

        _json[FAVORITES] = array;
        need_save = true;
    }

    if (need_save) {
        store();
    }

    return *this;
}

void PersistData::createDefault(bool store) {
    using namespace std;
    using namespace Wt;

    _json.clear();
    _json[UUID] = WString{Tools::gen_uuid()};
    _json[FULL_NAME] = WString{};
    _json[CITY] = WString{};
    _json[STREET] = WString{};
    _json[BUILDING] = WString{};
    _json[APARTMENT] = WString{};
    _json[PHONE] = WString{};
    _json[EMAIL] = WString{};
    _json[FAVORITES] = Json::Array{};

    if (store) {
        this->store();
    }
}

void PersistData::store() {
    using namespace std;
    using namespace Wt;

    auto jscript = format(R"(localStorage.)" PSDATANAME R"( = `{}`;)", Json::serialize(_json));
    WApplication::instance()->doJavaScript(jscript);
}
