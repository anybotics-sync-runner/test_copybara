################################ Master update #################################
core.workflow(
    name = "@(workflow)",

    origin = git.origin(url = "@(origin_url)", ref = "master", submodules = "NO", first_parent = True,),
    destination = git.destination(url = "@(destination_url)", fetch = "master", push = "master",),

    origin_files = glob(@(origin_paths), exclude = @(origin_excludes)),
    destination_files = glob(@(destination_paths), exclude = @(destination_excludes)),

    mode = "ITERATIVE",
    authoring = authoring.pass_thru(default = "@(default_author)"),
    transformations = [
        metadata.restore_author(label='ORIGINAL_AUTHOR', search_all_changes=True),
        @(transformations)
    ],
)
