################################ Branch import #################################
core.workflow(
    name = "@(workflow)",

    origin = git.origin(url = "@(origin_url)", ref = "none", submodules ="NO", first_parent = False,),
    destination = git.destination(url = "@(destination_url)", fetch = "master", push = "none",),

    origin_files = glob(@(origin_paths), exclude = @(origin_excludes)),
    destination_files = glob(@(destination_paths), exclude = @(destination_excludes)),

    mode = "CHANGE_REQUEST",
    authoring = authoring.pass_thru(default = "@(default_author)"),
    transformations = [
        metadata.replace_message("BEGIN_PUBLIC\n${COPYBARA_CURRENT_MESSAGE}\nEND_PUBLIC"),
        metadata.save_author(label='ORIGINAL_AUTHOR'),
        metadata.squash_notes(prefix="Changes for Project:\n", show_author = True, compact = False,),
        @(transformations)
    ],
)
