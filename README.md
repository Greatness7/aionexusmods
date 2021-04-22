
A simple python client for the Nexus Mods Public API.

---
```python
from aionexusmods import NexusMods

# Get your api key from the site preferences page.
# https://www.nexusmods.com/users/myaccount?tab=api

# Pass it in along with the game you're interested in.
async with NexusMods(API_KEY, "Morrowind") as nexusmods:
    
    # Check out your user info if you're curious.
    user = await nexusmods.get_user()
    print(f"Hello {user.name}!")

    # Or a particular mod that caught your attention.
    # https://www.nexusmods.com/morrowind/mods/46671
    mod = await nexusmods.get_mod(46671)
    assert mod.name == "Light Decay"
    assert mod.author == "Greatness7 and Melchior Dahrk"
    assert mod.available == True

    # See if there's any associated files or updates.
    files, updates = await nexusmods.get_files_and_updates(mod.mod_id)
    main_file = files[0]

    # You can also request download links for mod files.
    download_links = await nexusmods.get_download_links(mod.mod_id, main_file.file_id)
    main_mirror = download_links[0].URI

    # Premium users can even download directly from the api.
    await nexusmods.download(main_mirror, main_file.file_name)
    print(f"Download for '{main_file.file_name}' finished!")
```
---

Features an entirely async interface as well as structured return types and comprehensive annotations. Additionally this library takes care of finer details like download streams and rate limiting to help avoid wasting resources or exceeding API restrictions.


For more information see the official [Nexus Public API documentation](https://app.swaggerhub.com/apis-docs/NexusMods/nexus-mods_public_api_params_in_form_data/1.0).
