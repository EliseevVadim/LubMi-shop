#include "imageprocessor.h"
#include "config.h"
#include <Magick++.h>

std::expected<std::unique_ptr<Image>, std::string> ImageProcessor::createProductImage(const std::string &file, bool primary) {
    using namespace std;
    namespace Mg = Magick;

    try {
        Mg::Image img;
        Mg::Blob blob_img, blob_tmb;

        img.read(file);
        img.magick("JPEG");
        img.write(&blob_img);
        img.resize({THUMBNAIL_SIZE, THUMBNAIL_SIZE}, Mg::THUMBNAIL_FILTER);
        img.write(&blob_tmb);

        auto result = make_unique<Image>();
        result->primary = primary;
        result->format = ImageFormat::JPEG;
        result->image = blob_img.base64();
        result->thumbnail = blob_tmb.base64();

        return result;
    } catch (const exception &e) {
        return unexpected(e.what());
    }
}
