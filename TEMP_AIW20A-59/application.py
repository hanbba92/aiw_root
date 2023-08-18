import sys
import aiw_task_cm.common.initiator as common
import numpy as np
from aiw_task_cm.file.file_manager_factory import FileManagerFactory
from service.generate_surf import generate_surf
from service.GradientDescent import GradientDescent
from service.plot import plot

class Application(object):
    def __init__(self, workflow_id, input_file, PRMSL,initial_alpha, output_task):
        self.workflow_id = workflow_id
        self.input_file = input_file
        self.PRMSL = PRMSL
        self.initial_alpha = initial_alpha
        self.output_task = output_task

    def run(self):
        fm = FileManagerFactory().get_instance('netcdf')

        latitude, _ = fm.read(self.input_file, data_path='INPUTDATA/latitude')
        longitude, _ = fm.read(self.input_file, data_path='INPUTDATA/longitude')
        prmsl_all, _ = fm.read(self.input_file, data_path = self.PRMSL)
        y = np.arange(prmsl_all.shape[1])
        x = np.arange(prmsl_all.shape[2])
        XX, YY = np.meshgrid(x, y)

        u = XX.flatten()
        v = YY.flatten()
        lat = np.linspace(0.01, 0.99, 10)
        lon = np.linspace(0.01, 0.99, 10)
        result = np.zeros_like(prmsl_all)


        for i in range(0,prmsl_all.shape[0]):
            prmsl = prmsl_all[i]
            p = prmsl.flatten()
            surf = generate_surf(u, v, p)
            p_reversed = p * -1
            surf_reversed = generate_surf(u, v, p_reversed)
            print('surface calculated done')
            #high = []
            #low = []
            total = int(len(lat)*len(lon))
            count=0
            prmsl_threshold_low = np.median(prmsl) - np.std(prmsl) * 0.5
            prmsl_threshold_high = np.median(prmsl) + np.std(prmsl) * 0.5

            for y in lat:
                for x in lon:
                    ans, xr, yr = GradientDescent(prmsl, surf, np.array([y, x]), self.initial_alpha)

                    if ans:
                        iy, ix = xr[-1]
                        if yr[-1] <= prmsl_threshold_low:
              #              low.append([int(iy), int(ix)])

                            result[i, int(iy), int(ix)] = -1
                    count += 1
                    ans, xr, yr = GradientDescent(p_reversed, surf_reversed, np.array([y, x]), self.initial_alpha)

                    if ans:
                        iy, ix = xr[-1]
                        if yr[-1] <= prmsl_threshold_high * -1:
                            result[i, int(iy), int(ix)] = 1
             #               high.append([int(iy), int(ix)])
                    count += 1
                    print(f'{count}/{total} done')
            #self.Plot(self.input_data_path, low, high, i)

        #y = np.arange(0., prmsl_all.shape[1])
        #x = np.arange(0., prmsl_all.shape[2])
        fm.write([y, x, result], self.input_file, task_number=self.output_task,
                 data_type='flow', timed=True)


def main():
    workflow_id = sys.argv[1]
    input_file = sys.argv[2]
    PRMSL = sys.argv[3]
    initial_alpha = sys.argv[4]

    output_task = sys.argv[5]

    common.init('aiw-task-hr-' + output_task, workflow_id)
    result = 0
    try:
        app = Application(workflow_id, input_file, PRMSL, initial_alpha, output_task)
        app.run()
    except Exception as e:
        print(e)
        result = 1
    finally:
        sys.exit(result)


if __name__ == '__main__':
    main()
