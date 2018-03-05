import typing

from smac.tae.execute_ta_run_old import ExecuteTARunOld

__copyright__ = "Copyright 2018, ML4AAD"
__license__ = "3-clause BSD"
__maintainer__ = "Marius Lindauer"


class ExecuteTARunOldHydra(ExecuteTARunOld):

    """Returns min(cost, cost_portfolio)
    """
    
    def __init__(self, cost_oracle:typing.Mapping[str,float], **kwargs):
        '''
            Constructor
            
            Arguments
            ---------
            cost_oracle: typing.Mapping[str,float]
                cost of oracle per instance
        '''
        
        super().__init__(**kwargs)
        self.cost_oracle = cost_oracle

    def run(self, **kwargs):
        """ see ~smac.tae.execute_ta_run.ExecuteTARunOld for docstring
        """
        status, cost, runtime, additional_info = super(ExecuteTARunOldHydra,self).run(**kwargs)
        inst = kwargs["instance"]
        oracle_perf = self.cost_oracle.get(inst)
        if oracle_perf:
            # at this point, cost is not overwritten by runtime
            #TODO: This could be problematic for PAR10?
            if self.run_obj == "runtime":
                self.logger.debug("Portfolio perf: %f vs %f = %f" %(oracle_perf, runtime, min(oracle_perf,runtime)))
                runtime = min(oracle_perf,runtime)
            else:
                self.logger.debug("Portfolio perf: %f vs %f = %f" %(oracle_perf, cost, min(oracle_perf,cost)))
                cost = min(oracle_perf,cost)
            #TODO: update status?
        else:
            self.logger.error("Oracle performance missing --- should not happen")

        return status, cost, runtime, additional_info
    