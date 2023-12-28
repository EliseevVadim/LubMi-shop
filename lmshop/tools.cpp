#include "tools.h"
#include <filesystem>
#include <sstream>
#include <fstream>
#include <iostream>
#include <codecvt>
#include <locale>
#include <array>
#include <algorithm>
#include <map>
#include <boost/uuid/uuid.hpp>
#include <boost/uuid/uuid_generators.hpp>
#include <boost/uuid/uuid_io.hpp>
#include <Wt/WApplication.h>

std::string Tools::gen_uuid() noexcept {
    using namespace boost;
    static auto gen { uuids::random_generator() };
    return uuids::to_string(gen());
}

std::string Tools::read_stream(std::istream &ifs) {
    using namespace std;
    stringstream buff;
    return static_cast<stringstream &>(buff << ifs.rdbuf()).str();
}

std::string Tools::read_stream(const std::string &file) {
    using namespace std;
    ifstream f(file);
    return read_stream(f);
}

std::function<std::string (const std::string &)> Tools::create_transcoder(const std::string &code_page) {
    using namespace std;
    using namespace placeholders;
    using code_page_t = array<wchar_t, 256>;

    static const code_page_t cp_1251 {
        L'\u0000', L'\u0001', L'\u0002', L'\u0003', L'\u0004', L'\u0005', L'\u0006', L'\u0007',
        L'\u0008', L'\u0009', L'\u000A', L'\u000B', L'\u000C', L'\u000D', L'\u000E', L'\u000F',
        L'\u0010', L'\u0011', L'\u0012', L'\u0013', L'\u0014', L'\u0015', L'\u0016', L'\u0017',
        L'\u0018', L'\u0019', L'\u001A', L'\u001B', L'\u001C', L'\u001D', L'\u001E', L'\u001F',
        L'\u0020', L'\u0021', L'\u0022', L'\u0023', L'\u0024', L'\u0025', L'\u0026', L'\u0027',
        L'\u0028', L'\u0029', L'\u002A', L'\u002B', L'\u002C', L'\u002D', L'\u002E', L'\u002F',
        L'\u0030', L'\u0031', L'\u0032', L'\u0033', L'\u0034', L'\u0035', L'\u0036', L'\u0037',
        L'\u0038', L'\u0039', L'\u003A', L'\u003B', L'\u003C', L'\u003D', L'\u003E', L'\u003F',
        L'\u0040', L'\u0041', L'\u0042', L'\u0043', L'\u0044', L'\u0045', L'\u0046', L'\u0047',
        L'\u0048', L'\u0049', L'\u004A', L'\u004B', L'\u004C', L'\u004D', L'\u004E', L'\u004F',
        L'\u0050', L'\u0051', L'\u0052', L'\u0053', L'\u0054', L'\u0055', L'\u0056', L'\u0057',
        L'\u0058', L'\u0059', L'\u005A', L'\u005B', L'\u005C', L'\u005D', L'\u005E', L'\u005F',
        L'\u0060', L'\u0061', L'\u0062', L'\u0063', L'\u0064', L'\u0065', L'\u0066', L'\u0067',
        L'\u0068', L'\u0069', L'\u006A', L'\u006B', L'\u006C', L'\u006D', L'\u006E', L'\u006F',
        L'\u0070', L'\u0071', L'\u0072', L'\u0073', L'\u0074', L'\u0075', L'\u0076', L'\u0077',
        L'\u0078', L'\u0079', L'\u007A', L'\u007B', L'\u007C', L'\u007D', L'\u007E', L'\u007F',
        L'\u0402', L'\u0403', L'\u201A', L'\u0453', L'\u201E', L'\u2026', L'\u2020', L'\u2021',
        L'\u20AC', L'\u2030', L'\u0409', L'\u2039', L'\u040A', L'\u040C', L'\u040B', L'\u040F',
        L'\u0452', L'\u2018', L'\u2019', L'\u201C', L'\u201D', L'\u2022', L'\u2013', L'\u2014',
        L'\u0020', L'\u2122', L'\u0459', L'\u203A', L'\u045A', L'\u045C', L'\u045B', L'\u045F',
        L'\u00A0', L'\u040E', L'\u045E', L'\u0408', L'\u00A4', L'\u0490', L'\u00A6', L'\u00A7',
        L'\u0401', L'\u00A9', L'\u0404', L'\u00AB', L'\u00AC', L'\u00AD', L'\u00AE', L'\u0407',
        L'\u00B0', L'\u00B1', L'\u0406', L'\u0456', L'\u0491', L'\u00B5', L'\u00B6', L'\u00B7',
        L'\u0451', L'\u2116', L'\u0454', L'\u00BB', L'\u0458', L'\u0405', L'\u0455', L'\u0457',
        L'\u0410', L'\u0411', L'\u0412', L'\u0413', L'\u0414', L'\u0415', L'\u0416', L'\u0417',
        L'\u0418', L'\u0419', L'\u041A', L'\u041B', L'\u041C', L'\u041D', L'\u041E', L'\u041F',
        L'\u0420', L'\u0421', L'\u0422', L'\u0423', L'\u0424', L'\u0425', L'\u0426', L'\u0427',
        L'\u0428', L'\u0429', L'\u042A', L'\u042B', L'\u042C', L'\u042D', L'\u042E', L'\u042F',
        L'\u0430', L'\u0431', L'\u0432', L'\u0433', L'\u0434', L'\u0435', L'\u0436', L'\u0437',
        L'\u0438', L'\u0439', L'\u043A', L'\u043B', L'\u043C', L'\u043D', L'\u043E', L'\u043F',
        L'\u0440', L'\u0441', L'\u0442', L'\u0443', L'\u0444', L'\u0445', L'\u0446', L'\u0447',
        L'\u0448', L'\u0449', L'\u044A', L'\u044B', L'\u044C', L'\u044D', L'\u044E', L'\u044F',
    };

    static const code_page_t cp_1252 {
        L'\u0000', L'\u0001', L'\u0002', L'\u0003', L'\u0004', L'\u0005', L'\u0006', L'\u0007',
        L'\u0008', L'\u0009', L'\u000A', L'\u000B', L'\u000C', L'\u000D', L'\u000E', L'\u000F',
        L'\u0010', L'\u0011', L'\u0012', L'\u0013', L'\u0014', L'\u0015', L'\u0016', L'\u0017',
        L'\u0018', L'\u0019', L'\u001A', L'\u001B', L'\u001C', L'\u001D', L'\u001E', L'\u001F',
        L'\u0020', L'\u0021', L'\u0022', L'\u0023', L'\u0024', L'\u0025', L'\u0026', L'\u0027',
        L'\u0028', L'\u0029', L'\u002A', L'\u002B', L'\u002C', L'\u002D', L'\u002E', L'\u002F',
        L'\u0030', L'\u0031', L'\u0032', L'\u0033', L'\u0034', L'\u0035', L'\u0036', L'\u0037',
        L'\u0038', L'\u0039', L'\u003A', L'\u003B', L'\u003C', L'\u003D', L'\u003E', L'\u003F',
        L'\u0040', L'\u0041', L'\u0042', L'\u0043', L'\u0044', L'\u0045', L'\u0046', L'\u0047',
        L'\u0048', L'\u0049', L'\u004A', L'\u004B', L'\u004C', L'\u004D', L'\u004E', L'\u004F',
        L'\u0050', L'\u0051', L'\u0052', L'\u0053', L'\u0054', L'\u0055', L'\u0056', L'\u0057',
        L'\u0058', L'\u0059', L'\u005A', L'\u005B', L'\u005C', L'\u005D', L'\u005E', L'\u005F',
        L'\u0060', L'\u0061', L'\u0062', L'\u0063', L'\u0064', L'\u0065', L'\u0066', L'\u0067',
        L'\u0068', L'\u0069', L'\u006A', L'\u006B', L'\u006C', L'\u006D', L'\u006E', L'\u006F',
        L'\u0070', L'\u0071', L'\u0072', L'\u0073', L'\u0074', L'\u0075', L'\u0076', L'\u0077',
        L'\u0078', L'\u0079', L'\u007A', L'\u007B', L'\u007C', L'\u007D', L'\u007E', L'\u007F',
        L'\u20AC', L'\u0020', L'\u201A', L'\u0192', L'\u201E', L'\u2026', L'\u2020', L'\u2021',
        L'\u02C6', L'\u2030', L'\u0160', L'\u2039', L'\u0152', L'\u0020', L'\u017D', L'\u0020',
        L'\u0020', L'\u2018', L'\u2019', L'\u201C', L'\u201D', L'\u2022', L'\u2013', L'\u2014',
        L'\u02DC', L'\u2122', L'\u0161', L'\u203A', L'\u0153', L'\u0020', L'\u017E', L'\u0178',
        L'\u00A0', L'\u00A1', L'\u00A2', L'\u00A3', L'\u00A4', L'\u00A5', L'\u00A6', L'\u00A7',
        L'\u00A8', L'\u00A9', L'\u00AA', L'\u00AB', L'\u00AC', L'\u00AD', L'\u00AE', L'\u00AF',
        L'\u00B0', L'\u00B1', L'\u00B2', L'\u00B3', L'\u00B4', L'\u00B5', L'\u00B6', L'\u00B7',
        L'\u00B8', L'\u00B9', L'\u00BA', L'\u00BB', L'\u00BC', L'\u00BD', L'\u00BE', L'\u00BF',
        L'\u00C0', L'\u00C1', L'\u00C2', L'\u00C3', L'\u00C4', L'\u00C5', L'\u00C6', L'\u00C7',
        L'\u00C8', L'\u00C9', L'\u00CA', L'\u00CB', L'\u00CC', L'\u00CD', L'\u00CE', L'\u00CF',
        L'\u00D0', L'\u00D1', L'\u00D2', L'\u00D3', L'\u00D4', L'\u00D5', L'\u00D6', L'\u00D7',
        L'\u00D8', L'\u00D9', L'\u00DA', L'\u00DB', L'\u00DC', L'\u00DD', L'\u00DE', L'\u00DF',
        L'\u00E0', L'\u00E1', L'\u00E2', L'\u00E3', L'\u00E4', L'\u00E5', L'\u00E6', L'\u00E7',
        L'\u00E8', L'\u00E9', L'\u00EA', L'\u00EB', L'\u00EC', L'\u00ED', L'\u00EE', L'\u00EF',
        L'\u00F0', L'\u00F1', L'\u00F2', L'\u00F3', L'\u00F4', L'\u00F5', L'\u00F6', L'\u00F7',
        L'\u00F8', L'\u00F9', L'\u00FA', L'\u00FB', L'\u00FC', L'\u00FD', L'\u00FE', L'\u00FF',
    };

    static const map<string, const code_page_t &> codepages {
        {"ANSI_1251", cp_1251},
        {"ANSI_1252", cp_1252}
    };

    auto transcoder = [](const string & byte_str, const code_page_t &cpage)->string {
        if (byte_str.empty()) {
            return "";
        }

        wstring ucode_str(byte_str.size(), L' ');
        transform(byte_str.begin(), byte_str.end(), ucode_str.begin(), [&cpage](auto s) {
            return cpage[static_cast<uint8_t>(s)];
        });
        wstring_convert<codecvt_utf8<wchar_t>> ucode_to_utf8;
        return ucode_to_utf8.to_bytes(ucode_str);
    };

    return bind(transcoder, _1, codepages.at(code_page));
}

std::optional<std::string> Tools::get_string_option(const Wt::WEnvironment &env, const std::string &opt_name) {
    using namespace std;
    auto *value = env.getParameter(opt_name);
    return value ? optional{ *value } :
           optional<string> { };
}

std::optional<int> Tools::get_int_option(const Wt::WEnvironment &env, const std::string &opt_name) {
    using namespace std;
    auto value = get_string_option(env, opt_name);

    if (value) try {
            return stoi(*value);
        } catch (const invalid_argument &) {
            // return {};
        } catch (const out_of_range &) {
            // return {};
        }

    return {};
}

int Tools::get_int_option(const Wt::WEnvironment &env, const std::string &opt_name, int defv, int minv, int maxv) {
    using namespace std;
    return bound(get_int_option(env, opt_name).value_or(defv), minv, maxv);
}

std::optional<std::string> Tools::get_config_string(const std::string &name, bool empty_string_allowed) {
    using namespace std;
    using WApp = Wt::WApplication;

    string value;
    return (WApp::readConfigurationProperty(name, value) && (empty_string_allowed || !value.empty())) ? value : optional<string> {};
}

void Tools::for_each_file_do(const std::string &dir, std::function<void (const std::string &)> action) {
    using namespace std;
    using namespace filesystem;

    for (auto const &item : directory_iterator(path(dir))) {
        if (item.is_regular_file()) {
            action(item.path().string());
        }
    }
}
