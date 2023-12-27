#pragma once
#ifndef TOOLS_H
#define TOOLS_H

#include <dlfcn.h>
#include <format>
#include <string>
#include <istream>
#include <chrono>
#include <cmath>
#include <numbers>
#include <functional>
#include <optional>
#include <Wt/WEnvironment.h>
#include <Wt/WString.h>
#include <sys/resource.h>

class generator {
  public:
    generator(double x0, double h):
        a0{cos(x0 - h - h)},
        a1 {cos(x0 - h)},
        ch{2.0 * cos(h)} {
    }

    double operator()() const {
        auto a2 = a1 * ch - a0;
        a0 = a1;
        a1 = a2;
        return a2;
    }
  private:
    mutable double a0;
    mutable double a1;
    const double ch;

};

struct finalizer {
    explicit finalizer(std::function<void()> fin):
        fin_(fin) {
    }
    ~finalizer() {
        fin_();
    }
    std::function<void()> fin_;
};

class Tools final {
    Tools() = delete;

  public:
    static std::string read_stream(std::istream &ifs);
    static std::string read_stream(const std::string &file);
    static std::function<std::string(const std::string &)> create_transcoder(const std::string &code_page);
    static std::optional<std::string> get_string_option(const Wt::WEnvironment &env, const std::string &opt_name);
    static std::optional<int> get_int_option(const Wt::WEnvironment &env, const std::string &opt_name);
    static int get_int_option(const Wt::WEnvironment &env, const std::string &opt_name, int defv, int minv, int maxv);
    static std::optional<std::string> get_config_string(const std::string &name, bool empty_string_allowed = false);
    static void for_each_file_do(const std::string &dir, std::function<void(const std::string &file)> action);

    static inline void quota(rlim_t a, rlim_t b) {
        rlimit _ {a, b};
        setrlimit(RLIMIT_DATA, &_);
    }

    template<typename T, typename R>
    static inline R with_shlib_symbol_do(const std::string &file, int mode, const std::string &symbol, std::function<R (T(*)())> callback) {
        using namespace std;
        using namespace Wt;

        if (auto dlh = dlopen(file.c_str(), mode); dlh) {
            finalizer _f_([dlh] {
                dlclose(dlh);
            });

            if (auto pfunc = dlsym(dlh, symbol.c_str()); pfunc) {
                return callback(reinterpret_cast<T(*)()>(pfunc));
            } else {
                throw invalid_argument(WString::tr("msg-get-info-failed").toUTF8());
            }
        } else {
            throw invalid_argument(format("{}, {}!", WString::tr("msg-wrong-file").toUTF8(), dlerror()));
        }
    }

    template<typename T>
    static inline void with_shlib_symbol_do(const std::string &file, int mode, const std::string &symbol, std::function<void (T(*)())> callback) {
        with_shlib_symbol_do<T, int>(file, mode, symbol, [&callback](auto pfunc) {
            callback(pfunc);
            return 0;
        });
    }

    template<typename T> static T bound(T val, T leftb, T rightb) {
        using namespace std;
        return min(max(val, leftb), rightb);
    }

    template<typename T> static T lerp(T x, T a, T b, T c, T d) {
        using namespace std;
        return (c * (x - b) + d * (a - x)) / (a - b);
    }

    template<typename Entity, void(*deleter)(Entity *)> inline static std::unique_ptr<Entity, decltype(deleter)> makeHandle(Entity *eptr) {
        return { eptr, deleter };
    }
};

#endif // TOOLS_H
