#ifndef PERSISTINFO_H
#define PERSISTINFO_H

#include<string>
#include<list>
#include<Wt/WGlobal.h>
#include<Wt/WJavaScript.h>
#include<Wt/Json/Object.h>
#include<Wt/WApplication.h>

class PersistInfo final {
  public:
    PersistInfo();
    std::string uuid() const noexcept;
    PersistInfo &update(const std::optional<std::string> &full_name,
                        const std::optional<std::string> &city,
                        const std::optional<std::string> &street,
                        const std::optional<std::string> &building,
                        const std::optional<std::string> &apartment,
                        const std::optional<std::list<std::string>> &favorites);
  private:
    Wt::Json::Object json {};
    Wt::JSignal<std::string> sig_info_exists {Wt::WApplication::instance(), "info-exists"};
    Wt::JSignal<> sig_info_missed {Wt::WApplication::instance(), "info-missed"};
    void create_default(bool save = true);
    void save();
};

#endif // PERSISTINFO_H
