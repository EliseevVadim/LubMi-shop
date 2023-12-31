#include "imageprocessor.h"
#include "config.h"
#include <Magick++.h>

namespace Mg = Magick;

std::unique_ptr<Image> ImageProcessor::createProductImage(const std::string &file) {
    using namespace std;
    Mg::Image mgi;

    try {
        mgi.read(file);
        //TODO
    } catch (...) {
        return nullptr;
    }

    return make_unique<Image>();
}
