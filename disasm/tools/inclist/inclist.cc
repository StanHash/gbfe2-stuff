#include <string>
#include <vector>

#include <iostream>
#include <fstream>

char const * scan_whitespace(char const * str)
{
    while (*str != '\0' && std::isspace(*str))
        str++;

    return str;
}

char const * scan_quoted(char const * str)
{
    while (*str != '\0' && *str != '"')
        str++;

    return str;
}

char const * scan_word_or_fail(char const * str, char const * lower_word)
{
    while (*lower_word != '\0')
    {
        if (std::tolower(*str++) != *lower_word++)
            return nullptr;
    }

    return str;
}

bool scan(std::vector<std::string> & output, std::string const & filename)
{
    std::ifstream input(filename);

    if (!input.is_open())
        return false;

    std::string line;

    while (std::getline(input, line))
    {
        char const * str = line.c_str();

        str = scan_whitespace(str);
        str = scan_word_or_fail(str, "inc");

        if (str == nullptr)
            continue;

        char const * str_b = scan_word_or_fail(str, "lude");
        bool is_incbin = false;

        if (str_b == nullptr)
        {
            str_b = scan_word_or_fail(str, "bin");
            is_incbin = true;

            if (str_b == nullptr)
                continue;
        }

        str = scan_whitespace(str_b);

        if (*str++ != '"')
            continue;

        char const * str_end = scan_quoted(str);

        std::string included_filename(str, str_end);

        switch (is_incbin)
        {

        case false:
            scan(output, included_filename);

            [[fallthrough]];

        case true:
            output.push_back(std::move(included_filename));
            break;

        }
    }

    return true;
}

int main(int argc, char const * const * argv)
{
    if (argc != 2)
    {
        std::cerr << "Usage:" << std::endl;
        std::cerr << "  " << argv[0] << " INPUT" << std::endl;
        return 1;
    }

    std::string filename(argv[1]);
    std::vector<std::string> list;

    if (!scan(list, filename))
    {
        std::cerr << "Failed to open file `" << filename << "` for read." << std::endl;
        return 2;
    }

    for (std::string & str : list)
        std::cout << str << std::endl;

    return 0;
}
