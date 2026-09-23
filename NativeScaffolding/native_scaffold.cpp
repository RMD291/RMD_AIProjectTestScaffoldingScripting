#include <filesystem>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

namespace fs = std::filesystem;

struct Options {
    fs::path destination;
    std::string name;
    std::string kind = "project";
    std::string language = "cpp";
    std::string structure = "minimal";
    bool force = false;
};

using TemplateMap = std::map<std::string, std::string>;
using ValueMap = std::map<std::string, std::string>;

fs::path find_template_root(const fs::path& executable_path) {
    std::vector<fs::path> candidates;

    if (!executable_path.empty()) {
        candidates.push_back(executable_path.parent_path() / "templates");
        candidates.push_back(executable_path.parent_path().parent_path() / "templates");
    }

    candidates.push_back(fs::current_path() / "NativeScaffolding" / "templates");
    candidates.push_back(fs::current_path() / "templates");

    for (const auto& candidate : candidates) {
        if (fs::exists(candidate) && fs::is_directory(candidate)) {
            return candidate;
        }
    }

    throw std::runtime_error("cannot locate the native template directory");
}

std::string read_text_file(const fs::path& path) {
    std::ifstream input(path, std::ios::binary);
    if (!input) {
        throw std::runtime_error("cannot read " + path.string());
    }
    return std::string(std::istreambuf_iterator<char>(input), std::istreambuf_iterator<char>());
}

std::string render_text(const std::string& content, const ValueMap& values) {
    std::string rendered = content;
    for (const auto& [name, value] : values) {
        const std::string token = "{" + name + "}";
        std::size_t position = 0;
        while ((position = rendered.find(token, position)) != std::string::npos) {
            rendered.replace(position, token.size(), value);
            position += value.size();
        }
    }
    return rendered;
}

TemplateMap agent_templates() {
    return {
        {"AGENTS.md", "agent/AGENTS.md.tpl"},
        {".github/agents/project.agent.md", "agent/.github/agents/project.agent.md.tpl"},
        {".github/instructions/native.instructions.md", "agent/.github/instructions/native.instructions.md.tpl"},
        {".github/prompts/review.prompt.md", "agent/.github/prompts/review.prompt.md.tpl"},
        {".github/skills/project-context/SKILL.md", "agent/.github/skills/project-context/SKILL.md.tpl"},
    };
}

TemplateMap project_templates(const std::string& language, const std::string& structure) {
    const bool is_c = language == "c";
    const bool is_cpp = language == "cpp";
    const bool is_minimal = structure == "minimal";
    const bool is_production = structure == "production";
    const bool is_website = structure == "website";
    const bool is_mvc = structure == "mvc";

    if (!is_c && !is_cpp) {
        throw std::invalid_argument("native project language must be c or cpp");
    }
    if (!is_minimal && !is_production && !is_website && !is_mvc) {
        throw std::invalid_argument("structure must be minimal, production, website, or mvc");
    }

    const std::string source_name = is_c ? "main.c" : "main.cpp";
    const std::string source_template = is_c
        ? "project/minimal/c/main.c.tpl"
        : "project/minimal/cpp/main.cpp.tpl";

    TemplateMap templates;
    if (is_minimal) {
        templates["README.md"] = "project/minimal/README.md.tpl";
        templates[source_name] = source_template;
        return templates;
    }

    templates["README.md"] = "project/" + structure + "/README.md.tpl";
    templates[".gitignore"] = "project/" + structure + "/.gitignore.tpl";

    if (is_production) {
        templates["tests/README.md"] = "project/production/tests-README.md.tpl";
        templates["docs/README.md"] = "project/production/docs-README.md.tpl";
        templates["config/README.md"] = "project/production/config-README.md.tpl";
        templates["src/" + source_name] = source_template;
        return templates;
    }

    if (is_website) {
        templates["frontend/README.md"] = "project/website/frontend-README.md.tpl";
        templates["frontend/src/.gitkeep"] = "";
        templates["backend/README.md"] = "project/website/backend-README.md.tpl";
        templates["backend/src/.gitkeep"] = "";
        templates["database/README.md"] = "project/website/database-README.md.tpl";
        templates["database/migrations/.gitkeep"] = "";
        return templates;
    }

    templates["models/README.md"] = "project/mvc/models-README.md.tpl";
    templates["models/.gitkeep"] = "";
    templates["views/README.md"] = "project/mvc/views-README.md.tpl";
    templates["views/.gitkeep"] = "";
    templates["controllers/README.md"] = "project/mvc/controllers-README.md.tpl";
    templates["controllers/.gitkeep"] = "";
    templates["tests/README.md"] = "project/mvc/tests-README.md.tpl";
    templates["config/README.md"] = "project/mvc/config-README.md.tpl";
    return templates;
}

Options parse_options(int argc, char* argv[]) {
    if (argc < 2) {
        throw std::invalid_argument("destination is required");
    }

    Options options{fs::path(argv[1]), ""};
    for (int index = 2; index < argc; ++index) {
        const std::string argument = argv[index];
        const bool takes_value = argument == "--name"
            || argument == "--kind"
            || argument == "--language"
            || argument == "--structure";
        if (takes_value && index + 1 < argc && std::string(argv[index + 1]).rfind("--", 0) != 0) {
            const std::string value = argv[++index];
            if (argument == "--name") {
                options.name = value;
            } else if (argument == "--kind") {
                options.kind = value;
            } else if (argument == "--language") {
                options.language = value;
            } else if (argument == "--structure") {
                options.structure = value;
            }
        } else if (argument == "--force") {
            options.force = true;
        } else {
            throw std::invalid_argument("unknown or incomplete option: " + argument);
        }
    }

    if (options.name.empty()) {
        throw std::invalid_argument("--name is required");
    }

    return options;
}

ValueMap values_for_project(const std::string& name, const std::string& language) {
    const std::string language_label = language == "c" ? "C" : "C++";
    return {
        {"project_name", name},
        {"language_label", language_label},
        {"language_standard", language == "c" ? "C23" : "C++23"},
    };
}

ValueMap values_for_agent(const std::string& name) {
    return {{"project_name", name}};
}

std::map<std::string, std::string> render_templates(
    const fs::path& template_root,
    const TemplateMap& template_map,
    const ValueMap& values
) {
    std::map<std::string, std::string> rendered;
    for (const auto& [relative_path, template_path] : template_map) {
        if (template_path.empty()) {
            rendered[relative_path] = "";
            continue;
        }

        const fs::path source_path = template_root / template_path;
        const std::string content = read_text_file(source_path);
        rendered[relative_path] = render_text(content, values);
    }
    return rendered;
}

int generate(const Options& options, const fs::path& template_root) {
    if (options.kind != "agent" && options.kind != "project") {
        throw std::invalid_argument("kind must be agent or project");
    }

    const TemplateMap template_map = options.kind == "agent"
        ? agent_templates()
        : project_templates(options.language, options.structure);
    const ValueMap values = options.kind == "agent"
        ? values_for_agent(options.name)
        : values_for_project(options.name, options.language);

    const auto rendered = render_templates(template_root, template_map, values);

    std::size_t created = 0;
    std::size_t skipped = 0;

    for (const auto& [relative_path, content] : rendered) {
        const fs::path file_path = options.destination / relative_path;
        if (fs::exists(file_path) && !options.force) {
            std::cout << "SKIPPED: " << file_path.string() << '\n';
            ++skipped;
            continue;
        }

        if (!file_path.parent_path().empty()) {
            fs::create_directories(file_path.parent_path());
        }

        std::ofstream output(file_path, std::ios::binary);
        if (!output) {
            throw std::runtime_error("cannot write " + file_path.string());
        }

        output << content;
        std::cout << "CREATED: " << file_path.string() << '\n';
        ++created;
    }

    std::cout << "Generated " << created << " file(s); skipped " << skipped << " existing file(s).\n";
    return 0;
}

int main(int argc, char* argv[]) {
    try {
        const fs::path executable_path = fs::path(argv[0]);
        const fs::path template_root = find_template_root(executable_path);
        return generate(parse_options(argc, argv), template_root);
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        std::cerr << "Usage: native_scaffold <destination> --name <name> "
                  "[--kind agent|project] [--language c|cpp] "
                  "[--structure minimal|production|website|mvc] [--force]\n";
        return 2;
    }
}