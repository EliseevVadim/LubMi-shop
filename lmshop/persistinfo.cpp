#include "persistinfo.h"
#include "tools.h"
#include <format>
#include <list>

#include <Wt/Json/Array.h>
#include <Wt/Json/Serializer.h>
#include <Wt/Json/Parser.h>

PersistInfo::PersistInfo() {
    using namespace std;
    using namespace Wt;

    sig_info_exists.connect([this](const string & str) {
        try {
            Json::parse(str, json);
        } catch (WException) {
            create_default();
            return;
        }

        static const auto keys = {"uuid", "full_name", "city", "street", "building", "apartment", "favorites"};

        for (auto &key : keys) {
            if (!json.contains(key)) {
                create_default();
                break;
            }
        }

    });

    sig_info_missed.connect([this] {
        create_default();
    });

    auto js = format(R"(if(localStorage.lubmi_shop_persist_info) {{{}}} else {{{}}})",
                     sig_info_exists.createCall({"localStorage.lubmi_shop_persist_info"}),
                     sig_info_missed.createCall({}));
    WApplication::instance()->doJavaScript(js);
}

std::string PersistInfo::uuid() const noexcept {
    return {};
}

PersistInfo &PersistInfo::update(const std::optional<std::string> &full_name,
                                 const std::optional<std::string> &city,
                                 const std::optional<std::string> &street,
                                 const std::optional<std::string> &building,
                                 const std::optional<std::string> &apartment,
                                 const std::optional<std::list<std::string>> &favorites) {
    using namespace std;
    using namespace Wt;

    bool need_save = false;

    if (full_name) {
        json["full_name"] = WString(full_name.value());
        need_save = true;
    }

    if (city) {
        json["city"] = WString(city.value());
        need_save = true;
    }

    if (street) {
        json["street"] = WString(street.value());
        need_save = true;
    }

    if (building) {
        json["building"] = WString(building.value());
        need_save = true;
    }

    if (apartment) {
        json["apartment"] = WString(apartment.value());
        need_save = true;
    }

    if (favorites) {
        Json::Array array;

        for (const auto &str : favorites.value()) {
            array.emplace_back(str);
        }

        json["favorites"] = array;
        need_save = true;
    }

    if (need_save) {
        save();
    }

}

void PersistInfo::create_default(bool save) {
    using namespace std;
    using namespace Wt;

    json.clear();
    json["uuid"] = WString{Tools::gen_uuid()};
    json["full_name"] = WString{};
    json["city"] = WString{};
    json["street"] = WString{};
    json["building"] = WString{};
    json["apartment"] = WString{};
    json["favorites"] = Json::Array{};

    if (save) {
        this->save();
    }
}

void PersistInfo::save() {
    using namespace std;
    using namespace Wt;

    auto js = format(R"(localStorage.lubmi_shop_persist_info = `{}`;)", Json::serialize(json));
    WApplication::instance()->doJavaScript(js);
}
