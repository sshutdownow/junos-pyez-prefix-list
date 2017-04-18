# junos-pyez-prefix-list
create prefix-list from BGP routes with community

I have created this script to use it on BNG, as, at present time (15.1), DCU is not supported in dynamic profiles, though, SCU does.

Installation
------------
1. Install JunOS PyEZ library, please, [use official documentation](https://www.juniper.net/techpubs/en_US/junos-pyez2.0/topics/task/installation/junos-pyez-server-installing.html).
2. Enable **netconf** on Juniper device, please, [use official documentation](https://www.juniper.net/techpubs/en_US/junos-pyez2.0/topics/task/installation/junos-pyez-client-configuring.html)
3. Create ssh keys and account on Juniper host, please, [use official documentation](https://www.juniper.net/techpubs/en_US/junos-pyez2.0/topics/task/program/junos-pyez-authenticating-users-with-ssh-keys.html).
4. Download script, modify it to yours needs and **run**.

### Requirements

This script was tested to work under junos-eznc 2.1.1.

### Copyright

  Copyright (c) 2017 Igor Popov

License
-------
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

### Authors

  Igor Popov
  (ipopovi |at| gmail |dot| com)
