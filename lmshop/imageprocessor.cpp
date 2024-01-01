#include "imageprocessor.h"
#include "config.h"
#include <Magick++.h>

std::expected<std::unique_ptr<Image>, std::string> ImageProcessor::createProductImage(const std::string &file) {
    using namespace std;
    namespace Mg = Magick;

    try {
        Mg::Image mgi;
        mgi.read(file);
        //TODO process
        auto result = make_unique<Image>();
        //TODO setup result
        //return result;
        return unexpected{"fail"};
    } catch (const std::exception &e) {
        return unexpected(e.what());
    }
}
